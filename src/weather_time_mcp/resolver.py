"""Location resolution helpers."""

from weather_time_mcp.errors import AmbiguousLocationError, ValidationError
from weather_time_mcp.models import Location
from weather_time_mcp.open_meteo import OpenMeteoClient


class LocationResolver:
    """Resolve human-readable locations to Open-Meteo candidates."""

    def __init__(self, open_meteo: OpenMeteoClient) -> None:
        self.open_meteo = open_meteo

    def search(self, query: str, count: int | None = None) -> list[Location]:
        return self.open_meteo.search_locations(query, count=count)

    def resolve_one(self, query: str) -> Location:
        candidates = self.search(query)
        if not candidates:
            raise ValidationError(f"no location found for '{query}'")
        if len(candidates) == 1:
            return candidates[0]
        if is_ambiguous_location(query, candidates):
            raise AmbiguousLocationError(query, [candidate.to_dict() for candidate in candidates])
        return candidates[0]


def is_ambiguous_location(query: str, candidates: list[Location]) -> bool:
    """Return true when candidates need user clarification."""

    if len(candidates) <= 1:
        return False

    # Auto-select only when the first result is clearly dominant; otherwise
    # return candidates so the LLM can ask the user to clarify the place.
    normalized_query = query.strip().casefold()
    first = candidates[0]
    second = candidates[1]
    first_name_matches = first.name.casefold() == normalized_query
    second_name_matches = second.name.casefold() == normalized_query
    first_is_populated = first.population or 0
    second_is_populated = second.population or 0

    if first_name_matches and not second_name_matches:
        return False
    if first_is_populated >= max(second_is_populated * 10, 100_000):
        return False

    return True
