from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from .models import Campaign, CampaignItem
from .forms import CampaignForm, CampaignItemForm
from .services import generate_campaign_content

# --- Mixins for Authorization and Services ---

class UserOwnsCampaignMixin(UserPassesTestMixin):
    """
    Ensures that the user trying to access the object is the owner.
    Used for Campaign Detail, Update, and Delete views.
    """
    def test_func(self):
        campaign = self.get_object()
        return self.request.user == campaign.user

class UserOwnsCampaignItemMixin(UserPassesTestMixin):
    """
    Ensures the user owns the parent campaign of the item.
    Used for CampaignItem Update view.
    """
    def test_func(self):
        item = self.get_object()
        return self.request.user == item.campaign.user

class GeminiContentGeneratorMixin:
    """
    Mixin to handle the call to the Gemini service on form submission.
    """
    def form_valid(self, form):
        input_content = form.cleaned_data.get('input_content')
        if not input_content:
            messages.error(self.request, "Input content is required to generate a campaign.")
            return self.form_invalid(form)

        # Get campaign objectives from the parent campaign
        # This is safe because both Create and Update views ensure
        # form.instance.campaign is set before this is called.
        campaign_objectives = form.instance.campaign.objectives

        # Safely get organization objectives from the user's profile
        try:
            org_objectives = self.request.user.profile.org_objectives
        except AttributeError:
            org_objectives = None

        # Call the service to get the generated content
        generated_data = generate_campaign_content(
            input_content=input_content,
            org_context=org_objectives,
            campaign_context=campaign_objectives,
        )

        if generated_data:
            # If the service succeeds, populate the form instance with the new data
            for key, value in generated_data.items():
                setattr(form.instance, key, value)
            
            # Use the default success_message from the view
            # but you could customize it here if needed.
            # self.success_message = "Campaign item content generated and saved successfully!"
        else:
            # If the service fails, add an error and re-render the form
            messages.error(self.request, "There was an error generating content. Please check your API key and try again.")
            return self.form_invalid(form)
        
        return super().form_valid(form)

# --- Campaign Views (Unchanged) ---

class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'campaigns/campaign_list.html'
    context_object_name = 'campaigns'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(objectives__icontains=query))
        return queryset

class CampaignDetailView(LoginRequiredMixin, UserOwnsCampaignMixin, DetailView):
    model = Campaign
    template_name = 'campaigns/campaign_detail.html'
    context_object_name = 'campaign'

class CampaignCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign_form.html'
    success_message = "Campaign created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CampaignUpdateView(LoginRequiredMixin, UserOwnsCampaignMixin, SuccessMessageMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/campaign_form.html'
    success_message = "Campaign updated successfully!"

class CampaignDeleteView(LoginRequiredMixin, UserOwnsCampaignMixin, SuccessMessageMixin, DeleteView):
    model = Campaign
    template_name = 'campaigns/campaign_confirm_delete.html'
    success_url = reverse_lazy('campaign-list')
    success_message = "Campaign and all its items have been deleted successfully."

# --- Campaign Item Views (MODIFIED) ---

class CampaignItemCreateView(LoginRequiredMixin, GeminiContentGeneratorMixin, SuccessMessageMixin, CreateView):
    """
    Handles adding a new content item. Inherits from the Gemini mixin.
    """
    model = CampaignItem
    form_class = CampaignItemForm
    template_name = 'campaigns/campaign_item_form.html'
    success_message = "Campaign item content generated and saved successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign'] = get_object_or_404(Campaign, pk=self.kwargs['campaign_pk'])
        return context

    def form_valid(self, form):
        # First, assign the parent campaign before doing anything else
        campaign = get_object_or_404(Campaign, pk=self.kwargs['campaign_pk'])
        form.instance.campaign = campaign
        # Now, call the parent's (mixin's) form_valid to run the Gemini service
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.kwargs['campaign_pk']})

class CampaignItemUpdateView(LoginRequiredMixin, GeminiContentGeneratorMixin, UserOwnsCampaignItemMixin, SuccessMessageMixin, UpdateView):
    """
    Handles editing an existing campaign item. Inherits from the Gemini mixin.
    """
    model = CampaignItem
    form_class = CampaignItemForm
    template_name = 'campaigns/campaign_item_form.html'
    success_message = "Campaign item content regenerated and saved successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign'] = self.object.campaign
        return context
    
    def get_success_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.object.campaign.pk})