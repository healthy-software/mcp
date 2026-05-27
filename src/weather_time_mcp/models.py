"""Typed response models used by tools and clients."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Location:
    """A geocoded place candidate."""

    id: int | None
    name: str
    latitude: float
    longitude: float
    country: str | None = None
    country_code: str | None = None
    admin1: str | None = None
    timezone: str | None = None
    population: int | None = None

    @classmethod
    def from_open_meteo(cls, payload: dict[str, Any]) -> "Location":
        return cls(
            id=payload.get("id"),
            name=payload["name"],
            latitude=float(payload["latitude"]),
            longitude=float(payload["longitude"]),
            country=payload.get("country"),
            country_code=payload.get("country_code"),
            admin1=payload.get("admin1"),
            timezone=payload.get("timezone"),
            population=payload.get("population"),
        )

    def to_dict(self) -> dict[str, object]:
        return {key: value for key, value in asdict(self).items() if value is not None}
