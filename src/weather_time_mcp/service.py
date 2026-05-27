"""Application service used by MCP tools."""

from weather_time_mcp.config import DEFAULT_SETTINGS, Settings
from weather_time_mcp.errors import WeatherTimeMcpError
from weather_time_mcp.open_meteo import OpenMeteoClient
from weather_time_mcp.resolver import LocationResolver
from weather_time_mcp.time_now import TimeNowClient


class WeatherTimeService:
    """Coordinates API clients and MCP tool responses."""

    def __init__(
        self,
        open_meteo: OpenMeteoClient | None = None,
        time_now: TimeNowClient | None = None,
        settings: Settings = DEFAULT_SETTINGS,
    ) -> None:
        self.settings = settings
        self.open_meteo = open_meteo or OpenMeteoClient(settings=settings)
        self.time_now = time_now or TimeNowClient(settings=settings)
        self.resolver = LocationResolver(self.open_meteo)

    def search_locations(self, query: str, count: int | None = None) -> dict[str, object]:
        try:
            candidates = self.resolver.search(query, count=count)
        except WeatherTimeMcpError as exc:
            return exc.to_response()

        return {
            "ok": True,
            "provider": "Open-Meteo",
            "query": query,
            "locations": [candidate.to_dict() for candidate in candidates],
        }
