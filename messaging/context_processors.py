from accounts.selectors import get_profile_for_user
from .selectors import get_total_unread_count

def unread_count(request):
    """Context processor to add unread message count to all templates"""
    if not request.user.is_authenticated:
        return {'unread_message_count': 0}
        
    try:
        profile = get_profile_for_user(request.user)
        count = get_total_unread_count(profile)
        return {'unread_message_count': count}
    except Exception:
        # Fail silently if profile doesn't exist or other errors
        return {'unread_message_count': 0}
