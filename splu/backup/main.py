import argparse
import logging
from pathlib import Path

import splu.client
from splu.backup.albums import backup_albums
from splu.backup.playlists import backup_playlists
from splu.backup.tracks import backup_tracks

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Save a backup copy of a Spotify user's saved albums, playlists, tracks, etc.",
    )
    parser.add_argument("output_dir", type=Path, help="Directory path where the backup files will be saved.")
    args = parser.parse_args()

    client = splu.client.get(
        scopes=[
            "playlist-read-collaborative",
            "playlist-read-private",
            "user-library-read",
        ]
    )

    backup_albums(client=client, output_dir=args.output_dir)
    backup_playlists(client=client, output_dir=args.output_dir)
    backup_tracks(client=client, output_dir=args.output_dir)
