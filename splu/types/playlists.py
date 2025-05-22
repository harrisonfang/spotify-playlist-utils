from __future__ import annotations

from datetime import datetime
from typing import Optional

from splu.types.base import SpluType
from splu.types.images import Image
from splu.types.tracks import Track
from splu.types.users import User


class Playlist(SpluType):
    collaborative: bool
    description: str
    external_urls: dict[str, str]
    href: str
    id: str
    images: list[Image]
    name: str
    owner: User
    public: bool
    snapshot_id: str
    tracks: PlaylistTracks
    uri: str


class PlaylistTrack(SpluType):
    added_at: datetime
    added_by: User
    is_local: bool
    track: Track


class PlaylistTracks(SpluType):
    href: str
    total: int
