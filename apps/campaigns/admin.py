from django.contrib import admin
from .models import Campaign, CampaignItem

class CampaignItemInline(admin.TabularInline):
    """
    Allows editing CampaignItems directly within the Campaign admin page.
    """
    model = CampaignItem
    # Shows one extra empty form for adding a new item
    extra = 1
    # Fields to display in the inline form
    fields = ('title', 'input_content', 'image', 'video')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    Customizes the display for the Campaign model in the admin.
    """
    # The inline for CampaignItem is included here
    inlines = [CampaignItemInline]
    # Columns to display in the campaign list view
    list_display = ('title', 'user', 'updated_at', 'created_at')
    # Fields to search by
    search_fields = ('title', 'objectives', 'user__username')
    # Filters in the sidebar
    list_filter = ('user',)


@admin.register(CampaignItem)
class CampaignItemAdmin(admin.ModelAdmin):
    """
    Customizes the display for the CampaignItem model in the admin.
    """
    # Columns to display in the item list view
    list_display = ('title', 'campaign', 'updated_at')
    # Fields to search by, including the parent campaign's title
    search_fields = ('title', 'input_content', 'campaign__title')
    # Filters in the sidebar
    list_filter = ('campaign',)