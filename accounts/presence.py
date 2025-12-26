from django.core.cache import cache

ONLINE_TTL = 15  # seconds


def _presence_key(profile_id):
    return f"online:{profile_id}"


def mark_online(profile_id):
    cache.set(
        _presence_key(profile_id),
        True,
        timeout=ONLINE_TTL
    )


def is_online(profile_id):
    return cache.get(
        _presence_key(profile_id),
        False
    )
