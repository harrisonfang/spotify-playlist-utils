from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Optional

from pydantic import FieldSerializationInfo, field_serializer, model_validator

from splu.types.artists import Artist
from splu.types.base import SpluEnum, SpluType
from splu.types.images import Image

logger = logging.getLogger(__name__)


class Album(SpluType):
    album_type: AlbumType
    artists: list[Artist]
    available_markets: list
    external_urls: dict[str, str]
    href: str
    id: str
    images: list[Image]
    name: str
    release_date: Optional[date]
    release_date_precision: AlbumReleaseDatePrecision
    release_date_raw: str
    total_tracks: int
    uri: str

    @model_validator(mode="before")
    def parse_release_date(cls, data):
        release_date = data.get("release_date")
        release_date_precision = AlbumReleaseDatePrecision(data.get("release_date_precision"))

        match release_date_precision:
            case AlbumReleaseDatePrecision.DAY:
                parsed_release_date = date.fromisoformat(release_date)
            case AlbumReleaseDatePrecision.MONTH:
                parsed_release_date = datetime.strptime(release_date, "%Y-%m").date()
            case AlbumReleaseDatePrecision.YEAR:
                parsed_release_date = datetime.strptime(release_date, "%Y").date()
            case _:
                logger.warn(f"Encountered an unrecognized value: {release_date_precision=}")
                parsed_release_date = None

        data["release_date"] = parsed_release_date
        data["release_date_raw"] = release_date

        return data

    @field_serializer("release_date")
    def serialize_release_date(self, release_date: date, info: FieldSerializationInfo):
        return self.release_date_raw


class AlbumType(SpluEnum):
    UNKNOWN = ""
    ALBUM = "album"
    COMPILATION = "compilation"
    SINGLE = "single"


class AlbumReleaseDatePrecision(SpluEnum):
    UNKNOWN = ""
    DAY = "day"
    MONTH = "month"
    YEAR = "year"


class SavedAlbum(SpluType):
    added_at: datetime
    added_at_raw: str
    album: Album

    @model_validator(mode="before")
    def parse_added_at(cls, data):
        data["added_at_raw"] = data["added_at"]
        return data

    @field_serializer("added_at")
    def serialize_added_at(self, added_at: datetime, info: FieldSerializationInfo):
        return self.added_at_raw
