from django.db import models
from django.conf import settings
from django.urls import reverse

class Campaign(models.Model):
    """
    Represents a marketing or content campaign created by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    title = models.CharField(max_length=255)
    objectives = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # This is crucial for your home page requirement.
        # It ensures that by default, all queries for campaigns
        # will be ordered by the most recently updated.
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to the detail page for this campaign."""
        return reverse('campaign-detail', kwargs={'pk': self.pk})


class CampaignItem(models.Model):
    """
    Represents a single piece of content within a campaign.
    """
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='items'
    )
    title = models.CharField(max_length=255)
    
    # Content Fields
    input_content = models.TextField(help_text="The base content or brief for generation.")
    linkedin_content = models.TextField(blank=True, null=True)
    x_content = models.TextField(blank=True, null=True, verbose_name="X (Twitter) Content")
    facebook_content = models.TextField(blank=True, null=True)
    instagram_content = models.TextField(blank=True, null=True)
    youtube_content = models.TextField(blank=True, null=True, verbose_name="YouTube Description/Script")
    quora_content = models.TextField(blank=True, null=True)
    reddit_content = models.TextField(blank=True, null=True)
    blog_content = models.TextField(blank=True, null=True)

    # Prompt Fields
    image_prompt = models.TextField(blank=True, null=True)
    video_prompt = models.TextField(blank=True, null=True)
    
    # Media Fields
    image = models.ImageField(upload_to='campaign_images/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='campaign_videos/%Y/%m/%d/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Custom save method to update the parent campaign's timestamp.
        """
        # First, save the CampaignItem instance
        super().save(*args, **kwargs)
        # Then, trigger a save on the parent campaign to update its 'updated_at' field.
        # This makes the campaign "bubble up" to the top of the list.
        self.campaign.save()