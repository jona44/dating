from django.db.models.signals import post_save
from django.conf import settings
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(social_account_added)
def populate_profile_from_social(request, sociallogin, **kwargs):
    """
    Populate Profile with data from the social provider when a new account is linked.
    """
    user = sociallogin.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    data = sociallogin.account.extra_data
    
    if sociallogin.account.provider == 'google':
        if not profile.display_name:
            profile.display_name = data.get('name', '')
        # Profile picture handling could be added here if needed
        # profile.profile_picture = ...
        
    elif sociallogin.account.provider == 'facebook':
        if not profile.display_name:
            profile.display_name = data.get('name', '')
            
    profile.save()
