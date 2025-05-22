from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Optional

from pydantic import model_validator

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
        return data


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
