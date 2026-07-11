"""Location resolution and gazetteer helpers."""

from .resolve import (
    classify_trip_kind,
    is_domestic,
    resolve_coordinates,
    smart_destination_handler,
)

__all__ = [
    "smart_destination_handler",
    "is_domestic",
    "resolve_coordinates",
    "classify_trip_kind",
]
