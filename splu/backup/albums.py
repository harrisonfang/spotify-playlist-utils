import json
import logging
from pathlib import Path
from typing import cast

import spotipy
from pydantic.main import IncEx

import splu.iterate

logger = logging.getLogger(__name__)


_ALBUM_TRACK_FIELDS = cast(
    IncEx,
    {
        "artists": {
            "__all__": {
                "name",
            },
        },
        "disc_number": True,
        "duration_ms": True,
        "explicit": True,
        "name": True,
        "track_number": True,
    },
)


_SAVED_ALBUM_FIELDS = cast(
    IncEx,
    {
        "added_at": True,
        "album": {
            "album_type": True,
            "artists": {
                "__all__": {
                    "name",
                },
            },
            "name": True,
            "release_date": True,
            "release_date_precision": True,
            "total_tracks": True,
        },
    },
)


def backup_albums(*, client: spotipy.Spotify, output_dir: Path) -> None:
    """Save a backup copy of the current user's albums."""

    logger.info("Saving albums...")

    for saved_album in splu.iterate.saved_albums(client=client):
        album = saved_album.album
        logger.info(f"Saving album: {album.name} ({album.id})")

        album_dir = output_dir / "saved/albums" / f"{album.name} ({album.id})"
        album_dir.mkdir(parents=True, exist_ok=True)

        file_path = album_dir / "metadata.json"
        with open(file_path, "w") as f:
            json.dump(saved_album.model_dump(include=_SAVED_ALBUM_FIELDS), f, indent=2)

        album_tracks = []
        for album_track in splu.iterate.album_tracks(album.id, client=client):
            album_tracks.append(album_track.model_dump(include=_ALBUM_TRACK_FIELDS))

        file_path = album_dir / "tracks.json"
        with open(file_path, "w") as f:
            json.dump(album_tracks, f, indent=2)
