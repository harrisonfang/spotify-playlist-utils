from splu.types.base import SpluType


class Artist(SpluType):
    external_urls: dict[str, str]
    href: str
    id: str
    name: str
    uri: str
