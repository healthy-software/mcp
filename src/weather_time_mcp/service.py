"""Application service used by MCP tools."""

from weather_time_mcp.config import DEFAULT_SETTINGS, Settings
from weather_time_mcp.errors import ValidationError, WeatherTimeMcpError
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

    def get_current_weather(
        self,
        location: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict[str, object]:
        try:
            resolved_latitude, resolved_longitude, resolved_location = self._resolve_coordinates(
                location,
                latitude,
                longitude,
            )

            forecast = self.open_meteo.get_forecast(
                latitude=resolved_latitude,
                longitude=resolved_longitude,
                forecast_days=1,
                include_hourly=False,
            )
        except WeatherTimeMcpError as exc:
            return exc.to_response()

        return {
            "ok": True,
            "provider": "Open-Meteo",
            "resolved_location": resolved_location,
            "coordinates": forecast["coordinates"],
            "timezone": forecast["timezone"],
            "current": forecast["current"],
            "current_units": forecast["current_units"],
        }

    def _resolve_coordinates(
        self,
        location: str | None,
        latitude: float | None,
        longitude: float | None,
    ) -> tuple[float, float, dict[str, object] | None]:
        if location:
            candidate = self.resolver.resolve_one(location)
            return candidate.latitude, candidate.longitude, candidate.to_dict()
        if latitude is None or longitude is None:
            raise ValidationError("provide either location or both latitude and longitude")
        return latitude, longitude, None
