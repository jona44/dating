from interactions.models import Match
from .models import Conversation, Message
from django.utils import timezone
from .models import MessageRead



def get_or_create_conversation(profile_a, profile_b):
    # Ensure they are matched
    if not Match.objects.filter(profile1=profile_a, profile2=profile_b).exists() and \
       not Match.objects.filter(profile1=profile_b, profile2=profile_a).exists():
        raise PermissionDenied("Users are not matched")

    conversation = (
        Conversation.objects
        .filter(participants=profile_a)
        .filter(participants=profile_b)
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation.objects.create()
    conversation.participants.add(profile_a, profile_b)
    return conversation


def send_message(sender, conversation, body):
    if not conversation.participants.filter(id=sender.id).exists():
        raise PermissionDenied("Not a participant in this conversation")

    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        body=body
    )

    # Broadcast via WebSockets
    from django.template.loader import render_to_string
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    html = render_to_string('web/messaging/partials/message.html', {
        'message': message,
        'profile': None # Ensure recipient logic works
    })

    # Wrap in OOB swap for HTMX
    oob_html = f'<div id="messages" hx-swap-oob="beforeend">{html}</div>'

    async_to_sync(channel_layer.group_send)(
        f"chat_{conversation.id}",
        {
            "type": "chat_message",
            "id": str(message.id),
            "sender_id": str(sender.id),
            "message": message.body,
            "timestamp": message.created_at.isoformat(),
            "html": oob_html,
        }
    )

    return message


def mark_conversation_as_read(profile, conversation):
    messages = conversation.messages.exclude(sender=profile)

    for message in messages:
        MessageRead.objects.get_or_create(
            message=message,
            profile=profile
        )

