import os

import spotipy


def get(*, scopes: list[str]) -> spotipy.Spotify:
    """
    Initialize an authenticated spotipy client in headless mode (open_browser=False).

    In addition to the typical environment variables, we also add support for SPOTIPY_CACHE_PATH. This allows the caller
    to override the default cache location. If the cache exists, a client can be initialized automatically using the
    cache's refresh_token without manual authentication. However, requesting a new client with different scopes will
    invalidate the cache and require authentication again.
    """
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
