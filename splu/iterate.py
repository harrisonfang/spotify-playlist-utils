import functools
from typing import Iterator, Optional

import spotipy

import splu.client
from splu.types.albums import SavedAlbum
from splu.types.playlists import Playlist, PlaylistTrack, SavedTrack
from splu.types.tracks import Track

_ALBUM_TRACKS_PAGE_SIZE = 50
_PLAYLISTS_PAGE_SIZE = 50
_PLAYLIST_TRACKS_PAGE_SIZE = 100
_SAVED_ALBUMS_PAGE_SIZE = 50
_SAVED_TRACKS_PAGE_SIZE = 50


def album_tracks(album_id: str, *, client: Optional[spotipy.Spotify] = None) -> Iterator[Track]:
    """Iterate over the tracks in an album."""

    if not client:
        client = splu.client.get(scopes=[])

    offset = 0
    while True:
        response = client.album_tracks(album_id, limit=_ALBUM_TRACKS_PAGE_SIZE, offset=offset)
        for item in response["items"]:
            yield Track(**item)
        offset += _ALBUM_TRACKS_PAGE_SIZE
        if not response["next"]:
            break


def playlist_tracks(playlist_id: str, *, client: Optional[spotipy.Spotify] = None) -> Iterator[PlaylistTrack]:
    """Iterate over the tracks in a playlist."""

    if not client:
        client = splu.client.get(scopes=[])

    offset = 0
    while True:
        response = client.playlist_tracks(playlist_id, limit=_PLAYLIST_TRACKS_PAGE_SIZE, offset=offset)
        for item in response["items"]:
            yield PlaylistTrack(**item)
        offset += _PLAYLIST_TRACKS_PAGE_SIZE
        if not response["next"]:
            break


def saved_albums(*, client: Optional[spotipy.Spotify] = None) -> Iterator[SavedAlbum]:
    """Iterate over the current user's saved albums (i.e. Added to Library)."""

    if not client:
        client = splu.client.get(scopes=["user-library-read"])

    offset = 0
    while True:
        response = client.current_user_saved_albums(limit=_SAVED_ALBUMS_PAGE_SIZE, offset=offset)
        for item in response["items"]:
            yield SavedAlbum(**item)
        offset += _SAVED_ALBUMS_PAGE_SIZE
        if not response["next"]:
            break


def saved_tracks(*, client: Optional[spotipy.Spotify] = None) -> Iterator[SavedTrack]:
    """Iterate over the current user's saved tracks (i.e. Liked Songs)."""

    if not client:
        client = splu.client.get(scopes=["user-library-read"])

    offset = 0
    while True:
        response = client.current_user_saved_tracks(limit=_SAVED_TRACKS_PAGE_SIZE, offset=offset)
        for item in response["items"]:
            yield SavedTrack(**item)
        offset += _SAVED_TRACKS_PAGE_SIZE
        if not response["next"]:
            break


def user_playlists(user_id: str = "", *, client: Optional[spotipy.Spotify] = None) -> Iterator[Playlist]:
    """
    Iterate over a user's playlists.

    If user_id is not provided, then it is assumed to be the current user. By default, this will only yield a user's
    public playlists. The behavior can be changed by passing in a client with additional scopes such as
    playlist-read-collaborative and playlist-read-private.
    """

    if not client:
        client = splu.client.get(scopes=[])

    if user_id:
        request_fn = functools.partial(client.user_playlists, user_id)
    else:
        request_fn = client.current_user_playlists

    offset = 0
    while True:
        response = request_fn(limit=_PLAYLISTS_PAGE_SIZE, offset=offset)
        for item in response["items"]:
            yield Playlist(**item)
        offset += _PLAYLISTS_PAGE_SIZE
        if not response["next"]:
            break
