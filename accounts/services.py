from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Profile


def deactivate_account(user):
    user.is_active = False
    user.save(update_fields=['is_active'])


def verify_profile(profile):
    profile.is_verified = True
    profile.save(update_fields=['is_verified'])


def set_profile_visibility(profile, visible: bool):
    profile.is_visible = visible
    profile.save(update_fields=['is_visible'])

def update_last_seen(profile):
    profile.last_seen = timezone.now()
    profile.save(update_fields=['last_seen'])
