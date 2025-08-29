from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extends the default User model to include organization-specific details.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    org_name = models.CharField(max_length=255, blank=True, null=True)
    org_objectives = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# --- Django Signals to auto-create/update Profile ---

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    A signal to automatically create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    A signal to save the Profile whenever the User object is saved.
    """
    instance.profile.save()