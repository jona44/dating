from django.core.cache import cache

TYPING_TTL = 6  # seconds


def _typing_key(conversation_id, profile_id):
    return f"typing:{conversation_id}:{profile_id}"


def set_typing(conversation_id, profile_id):
    cache.set(
        _typing_key(conversation_id, profile_id),
        True,
        timeout=TYPING_TTL
    )


def is_typing(conversation_id, profile_id):
    return cache.get(
        _typing_key(conversation_id, profile_id),
        False
    )
