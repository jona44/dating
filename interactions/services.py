from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Like, Match, Block, Report, Skip
from messaging.models import Conversation
from accounts.models import Profile


@transaction.atomic
def handle_like(from_profile: Profile, to_profile: Profile):
    if from_profile == to_profile:
        return None
    
    # Don't allow liking blocked users
    if is_blocked(from_profile, to_profile):
        return None

    like, created = Like.objects.get_or_create(
        from_profile=from_profile,
        to_profile=to_profile
    )

    if not created:
        return None  # already liked

    reciprocal = Like.objects.filter(
        from_profile=to_profile,
        to_profile=from_profile
    ).exists()

    if reciprocal:
        p1, p2 = sorted([from_profile, to_profile], key=lambda p: p.id)

        match, match_created = Match.objects.get_or_create(
            profile1=p1,
            profile2=p2
        )

        if match_created:
            conversation = Conversation.objects.create()
            conversation.participants.add(p1, p2)
            
            # Send match notification emails
            from accounts.emails import send_match_notification_email
            send_match_notification_email(p1.user, p2)
            send_match_notification_email(p2.user, p1)

        return match

    return None


def skip_user(from_profile: Profile, to_profile: Profile):
    """Skip a user to avoid showing them in discovery"""
    if from_profile == to_profile:
        return None
    
    skip, created = Skip.objects.get_or_create(
        from_profile=from_profile,
        to_profile=to_profile
    )
    return skip


def block_user(blocker: Profile, blocked: Profile):
    """Block a user and remove any existing matches/likes"""
    if blocker == blocked:
        return None
    
    # Create block
    block, created = Block.objects.get_or_create(
        blocker=blocker,
        blocked=blocked
    )
    
    # Remove any existing likes
    Like.objects.filter(from_profile=blocker, to_profile=blocked).delete()
    Like.objects.filter(from_profile=blocked, to_profile=blocker).delete()
    
    # Remove matches
    Match.objects.filter(profile1=blocker, profile2=blocked).delete()
    Match.objects.filter(profile1=blocked, profile2=blocker).delete()
    
    return block


def unblock_user(blocker: Profile, blocked: Profile):
    """Unblock a user"""
    Block.objects.filter(blocker=blocker, blocked=blocked).delete()


def is_blocked(profile1: Profile, profile2: Profile):
    """Check if either user has blocked the other"""
    return Block.objects.filter(
        blocker=profile1, blocked=profile2
    ).exists() or Block.objects.filter(
        blocker=profile2, blocked=profile1
    ).exists()


def report_user(reporter: Profile, reported: Profile, reason: str, description: str = ""):
    """Report a user for inappropriate behavior"""
    if reporter == reported:
        return None
    
    return Report.objects.create(
        reporter=reporter,
        reported=reported,
        reason=reason,
        description=description
    )


def record_profile_view(viewer: Profile, viewed: Profile):
    """Record a profile view, avoiding duplicates within a short period"""
    if viewer == viewed:
        return None
    
    from .models import ProfileView
    from django.utils import timezone
    from datetime import timedelta

    # Check for a very recent view to deduplicate (e.g., within 1 hour)
    recent_view = ProfileView.objects.filter(
        viewer=viewer,
        viewed=viewed,
        created_at__gt=timezone.now() - timedelta(hours=1)
    ).exists()

    if not recent_view:
        return ProfileView.objects.create(viewer=viewer, viewed=viewed)
    
    return None
