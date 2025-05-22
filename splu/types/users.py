from typing import Optional

from splu.types.base import SpluType


class User(SpluType):
    display_name: Optional[str] = None
    external_urls: dict[str, str]
    href: str
    id: str
    uri: str
