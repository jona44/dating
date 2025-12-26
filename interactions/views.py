from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from .models import Like, Match


from accounts.selectors import get_profile_for_user
from .services import handle_like, skip_user

@login_required
def like_user_view(request, user_id):
    # This view seems to be for liking by User ID, possibly from an old API or HTMX call.
    # We'll adapt it to use profiles.
    actor_profile = get_profile_for_user(request.user)
    target_profile = get_object_or_404(Profile, user_id=user_id)

    match = handle_like(actor_profile, target_profile)

    if match:
        return HttpResponse("MATCH 💖")
    
    return HttpResponse("LIKED")


@login_required
def skip_user_view(request, user_id):
    """Handle skipping a user via HTMX"""
    actor_profile = get_profile_for_user(request.user)
    target_profile = get_object_or_404(Profile, user_id=user_id)

    skip_user(actor_profile, target_profile)
    
    return HttpResponse("SKIPPED")



