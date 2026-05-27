import pytest

from weather_time_mcp.errors import AmbiguousLocationError
from weather_time_mcp.models import Location
from weather_time_mcp.resolver import LocationResolver, is_ambiguous_location


class FakeOpenMeteo:
    def __init__(self, locations):
        self.locations = locations

    def search_locations(self, query, count=None):  # noqa: ANN001
        return self.locations


def test_resolver_returns_single_candidate():
    location = Location(id=1, name="Pune", latitude=18.52, longitude=73.85, timezone="Asia/Kolkata")
    resolver = LocationResolver(FakeOpenMeteo([location]))

    assert resolver.resolve_one("Pune") == location


def test_resolver_raises_for_ambiguous_candidates():
    resolver = LocationResolver(
        FakeOpenMeteo(
            [
                Location(id=1, name="Springfield", latitude=39.8, longitude=-89.6, population=100_000),
                Location(id=2, name="Springfield", latitude=44.0, longitude=-123.0, population=80_000),
            ]
        )
    )

    with pytest.raises(AmbiguousLocationError):
        resolver.resolve_one("Springfield")


def test_population_gap_can_make_first_candidate_unambiguous():
    candidates = [
        Location(id=1, name="London", latitude=51.5, longitude=-0.1, population=8_000_000),
        Location(id=2, name="London", latitude=42.9, longitude=-81.2, population=400_000),
    ]

    assert is_ambiguous_location("London", candidates) is False
