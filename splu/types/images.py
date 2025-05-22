from typing import Optional

from splu.types.base import SpluType


class Image(SpluType):
    height: Optional[int]
    width: Optional[int]
    url: str
