from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import FieldSerializationInfo, field_serializer, model_validator

from splu.types.albums import Album
from splu.types.artists import Artist
from splu.types.base import SpluType


class SavedTrack(SpluType):
    added_at: datetime
    added_at_raw: str
    track: Optional[Track] = None

    @model_validator(mode="before")
    def parse_added_at(cls, data):
        data["added_at_raw"] = data["added_at"]
        return data

    @field_serializer("added_at")
    def serialize_added_at(self, added_at: datetime, info: FieldSerializationInfo):
        return self.added_at_raw


class Track(SpluType):
    album: Optional[Album] = None
    artists: list[Artist]
    available_markets: list
    disc_number: int
    duration_ms: int
    episode: Optional[bool] = None
    explicit: bool
    external_ids: Optional[dict[str, str]] = None
    external_urls: dict[str, str]
    href: str
    id: str
    is_local: bool
    name: str
    popularity: Optional[int] = None
    track: Optional[bool] = None
    track_number: int
    uri: str


SavedTrack.model_rebuild()
