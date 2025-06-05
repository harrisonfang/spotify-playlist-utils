from __future__ import annotations

from splu.types.base import SpluType
from splu.types.images import Image
from splu.types.tracks import SavedTrack, Track
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


class PlaylistTrack(SavedTrack):
    added_by: User
    is_local: bool


class PlaylistTracks(SpluType):
    href: str
    total: int
