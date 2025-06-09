import json
import logging
from pathlib import Path
from typing import cast

import spotipy
from pydantic.main import IncEx

import splu.iterate

logger = logging.getLogger(__name__)


_SAVED_TRACK_FIELDS = cast(
    IncEx,
    {
        "added_at": True,
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


def backup_tracks(*, client: spotipy.Spotify, output_dir: Path) -> None:
    """Save a backup copy of the current user's tracks."""

    logger.info("Saving tracks...")

    file_path = output_dir / "saved/tracks.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    saved_tracks = []
    for saved_track in splu.iterate.saved_tracks(client=client):
        saved_tracks.append(saved_track.model_dump(include=_SAVED_TRACK_FIELDS))

    with open(file_path, "w") as f:
        json.dump(saved_tracks, f, indent=2)
