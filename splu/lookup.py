import functools
from typing import MutableMapping, Optional

import spotipy
from cachetools import TTLCache as TtlCache

import splu.client
from splu.types.users import User

_user_cache: MutableMapping[str, User] = TtlCache(maxsize=128, ttl=60)


def user(user_id: str = "", *, client: Optional[spotipy.Spotify] = None, use_cache: bool = False) -> User:
    """Get info about the given user."""

    if not client:
        client = splu.client.get(scopes=[])

    if user_id:
        cache_key = user_id
        client_fn = functools.partial(client.user, user_id)
    else:
        cache_key = client
        client_fn = client.current_user

    if not use_cache:
        _user_cache.pop(cache_key, None)

    if cache_key not in _user_cache:
        user = User(**client_fn())
        if cache_key != user.id:
            _user_cache[user.id] = user
        _user_cache[cache_key] = user

    return _user_cache[cache_key]
