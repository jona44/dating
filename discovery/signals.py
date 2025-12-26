from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from .models import Preference


@receiver(post_save, sender=Profile)
def create_preferences(sender, instance, created, **kwargs):
    """Auto-create preferences when a profile is created"""
    if created:
        Preference.objects.get_or_create(profile=instance)
