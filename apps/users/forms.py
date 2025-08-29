from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    A form for user registration that includes an email field.
    Inherits from UserCreationForm to get password validation and user creation logic.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """
    A form to update the user's profile information.
    Widgets are customized to apply Tailwind CSS classes for styling.
    """
    class Meta:
        model = Profile
        fields = ['org_name', 'org_objectives']
        widgets = {
            'org_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'org_objectives': forms.Textarea(attrs={
                'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'rows': 4
            }),
        }