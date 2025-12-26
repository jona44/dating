from .models import Conversation, Message, MessageRead
from django.db.models import Count, Q, Max, Exists, OuterRef


def get_conversations_for_profile(profile):
    """Get all conversations for a profile"""
    return Conversation.objects.filter(participants=profile).order_by('-created_at')


def get_conversation(conversation_id):
    """Get a specific conversation"""
    return Conversation.objects.get(id=conversation_id)


def get_messages_with_read_state(conversation, for_profile):
    """Get messages with read state for a specific profile"""
    messages = conversation.messages.select_related('sender').all()
    
    for message in messages:
        message.is_read_by_me = MessageRead.objects.filter(
            message=message,
            profile=for_profile
        ).exists()
    
    return messages


def get_unread_count_for_conversation(conversation, profile):
    """Get count of unread messages in a conversation for a specific profile"""
    return Message.objects.filter(
        conversation=conversation
    ).exclude(
        sender=profile
    ).exclude(
        reads__profile=profile
    ).count()


def get_total_unread_count(profile):
    """Get total unread message count across all conversations"""
    return Message.objects.filter(
        conversation__participants=profile
    ).exclude(
        sender=profile
    ).exclude(
        reads__profile=profile
    ).count()


def get_conversations_with_unread_counts(profile):
    """Get conversations annotated with unread message counts"""
    conversations = Conversation.objects.filter(
        participants=profile
    ).annotate(
        last_message_time=Max('messages__created_at'),
        unread_count=Count(
            'messages',
            filter=Q(messages__reads__profile__isnull=True) & ~Q(messages__sender=profile)
        )
    ).order_by('-last_message_time')
    
    return conversations
