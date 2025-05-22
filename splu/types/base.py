import logging
from enum import Enum

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SpluEnum(str, Enum):
    """
    Base class for all enums in this package.

    It's recommended to use this in cases where the API returns a predetermined set of string values. To gracefully
    handle API changes (e.g. new values), all subclasses should define an UNKNOWN value which will be the default.
    """

    @classmethod
    def _missing_(cls, value):
        logger.warn(f"Encountered an unrecognized value {cls}: {value}")
        return cls.UNKNOWN


class SpluType(BaseModel):
    """
    Base class for all types in this package

    Subclasses should generally avoid using Optional/None unless necessary (e.g. some APIs may omit certain fields).
    It may even be reasonable to set empty default values in such cases. The only caveat is when such a value could
    have a meaningful interpretation (e.g. zero or false).
    """

    class Config:
        pass
