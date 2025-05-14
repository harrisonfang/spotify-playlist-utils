import os

import spotipy


def get(*, scopes: list[str]) -> spotipy.Spotify:
    return spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            cache_handler=spotipy.oauth2.CacheFileHandler(
                cache_path=os.environ.get("SPOTIPY_CACHE_PATH"),
            ),
            client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
            open_browser=False,
            scope=scopes,
        )
    )
