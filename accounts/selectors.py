from .models import Profile
from .presence import is_online


def get_visible_profiles():
    return Profile.objects.filter(
        is_visible=True,
        user__is_active=True
    )


def get_profile_for_user(user):
    return Profile.objects.select_related('user').get(user=user)


def get_presence_map(profiles):
    return {
        profile.id: is_online(profile.id)
        for profile in profiles
    }
