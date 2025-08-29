from django import forms
from .models import Campaign, CampaignItem

# --- Reusable Widget Attributes for consistent styling ---

common_text_input_attrs = {
    'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
}

common_textarea_attrs = {
    'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    'rows': 5
}

common_file_input_attrs = {
    'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
}


class CampaignForm(forms.ModelForm):
    """
    Form for creating and updating a Campaign.
    """
    class Meta:
        model = Campaign
        fields = ['title', 'objectives']
        widgets = {
            'title': forms.TextInput(attrs=common_text_input_attrs),
            'objectives': forms.Textarea(attrs=common_textarea_attrs),
        }


class CampaignItemForm(forms.ModelForm):
    """
    Form for creating and updating a CampaignItem.
    """
    class Meta:
        model = CampaignItem
        fields = [
            'title', 'input_content', 'linkedin_content', 'x_content', 
            'facebook_content', 'instagram_content', 'youtube_content', 
            'quora_content', 'reddit_content', 'blog_content', 
            'image_prompt', 'video_prompt', 'image', 'video'
        ]
        widgets = {
            'title': forms.TextInput(attrs=common_text_input_attrs),
            'input_content': forms.Textarea(attrs={**common_textarea_attrs, 'rows': 8}),
            'linkedin_content': forms.Textarea(attrs=common_textarea_attrs),
            'x_content': forms.Textarea(attrs=common_textarea_attrs),
            'facebook_content': forms.Textarea(attrs=common_textarea_attrs),
            'instagram_content': forms.Textarea(attrs=common_textarea_attrs),
            'youtube_content': forms.Textarea(attrs=common_textarea_attrs),
            'quora_content': forms.Textarea(attrs=common_textarea_attrs),
            'reddit_content': forms.Textarea(attrs=common_textarea_attrs),
            'blog_content': forms.Textarea(attrs={**common_textarea_attrs, 'rows': 12}),
            'image_prompt': forms.Textarea(attrs={**common_textarea_attrs, 'rows': 2}),
            'video_prompt': forms.Textarea(attrs={**common_textarea_attrs, 'rows': 2}),
            'image': forms.ClearableFileInput(attrs=common_file_input_attrs),
            'video': forms.ClearableFileInput(attrs=common_file_input_attrs),
        }