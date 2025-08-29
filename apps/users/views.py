from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile
from .forms import UserRegisterForm, ProfileUpdateForm

class RegisterView(SuccessMessageMixin, CreateView):
    """
    Handles user registration. On successful registration, redirects to the login page.
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your account was created successfully! You can now log in."

class CustomLoginView(SuccessMessageMixin, LoginView):
    """
    Handles user login. The template will be rendered with the form.
    """
    template_name = 'users/login.html'
    # The success_url is handled by the LOGIN_REDIRECT_URL setting in settings.py

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Handles viewing and updating the user's profile information.
    Ensures that only the logged-in user can access and edit their own profile.
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Your profile has been updated successfully."

    def get_object(self, queryset=None):
        """
        This crucial method ensures that the user can only edit their own profile.
        It fetches the profile object associated with the currently logged-in user.
        """
        return self.request.user.profile