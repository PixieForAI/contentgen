from django.urls import path
from .views import (
    CampaignListView,
    CampaignDetailView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDeleteView,
    CampaignItemCreateView,
    CampaignItemUpdateView,
)

# This urls.py is included from the project's main urls.py
# The empty path '' is the root of the app.

urlpatterns = [
    # Campaign URLs
    path('', CampaignListView.as_view(), name='campaign-list'),
    path('campaign/create/', CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaign/<int:pk>/edit/', CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaign/<int:pk>/delete/', CampaignDeleteView.as_view(), name='campaign-delete'),

    # Campaign Item URLs
    path('campaign/<int:campaign_pk>/item/create/', CampaignItemCreateView.as_view(), name='campaign-item-create'),
    path('item/<int:pk>/edit/', CampaignItemUpdateView.as_view(), name='campaign-item-update'),
]