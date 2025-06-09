import json
import logging
from pathlib import Path
from typing import cast

import spotipy
from pydantic.main import IncEx

import splu.iterate
import splu.lookup
from splu.types.users import User

logger = logging.getLogger(__name__)


_PLAYLIST_FIELDS = cast(
    IncEx,
    {
        "collaborative": True,
        "description": True,
        "name": True,
        "owner": {
            "display_name",
        },
        "public": True,
        "tracks": {
            "total",
        },
    },
)


_PLAYLIST_TRACK_FIELDS = cast(
    IncEx,
    {
        "added_at": True,
        "added_by": {
            "display_name",
        },
        "track": {
            "album": {
                "name",
            },
            "artists": {
                "__all__": {
                    "name",
                }
            },
            "duration_ms": True,
            "explicit": True,
            "name": True,
        },
    },
)


def backup_playlists(*, client: spotipy.Spotify, output_dir: Path) -> None:
    """Save a backup copy of the current user's playlists."""

    logger.info("Saving playlists...")

    user_id = splu.lookup.user().id
    owned_playlists_dir = output_dir / "playlists"
    saved_playlists_dir = output_dir / "saved/playlists"

    for playlist in splu.iterate.user_playlists(client=client):
        logger.info(f"Saving playlist: {playlist.name} ({playlist.id})")

        playlist_dir = owned_playlists_dir if playlist.owner.id == user_id else saved_playlists_dir
        playlist_dir = playlist_dir / f"{playlist.name} ({playlist.id})"
        playlist_dir.mkdir(parents=True, exist_ok=True)

        file_path = playlist_dir / "metadata.json"
        with open(file_path, "w") as f:
            json.dump(playlist.model_dump(include=_PLAYLIST_FIELDS), f, indent=2)

        playlist_tracks = []
        for playlist_track in splu.iterate.playlist_tracks(playlist.id, client=client):
            # Unfortunately, `display_name` is not populated in the API response so we do a separate lookup.
            playlist_track.added_by.display_name = splu.lookup.user(
                playlist_track.added_by.id, use_cache=True
            ).display_name
            playlist_tracks.append(playlist_track.model_dump(include=_PLAYLIST_TRACK_FIELDS))

        file_path = playlist_dir / "tracks.json"
        with open(file_path, "w") as f:
            json.dump(playlist_tracks, f, indent=2)
