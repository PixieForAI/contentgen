from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Profile model in the Django admin.
    """
    list_display = ('user', 'org_name')
    search_fields = ('user__username', 'org_name')