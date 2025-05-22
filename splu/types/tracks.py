from splu.types.albums import Album
from splu.types.artists import Artist
from splu.types.base import SpluType


class Track(SpluType):
    album: Album
    artists: list[Artist]
    available_markets: list
    disc_number: int
    duration_ms: int
    episode: bool
    explicit: bool
    external_ids: dict[str, str]
    external_urls: dict[str, str]
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    track: bool
    track_number: int
    uri: str
