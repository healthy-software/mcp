"""Application service used by MCP tools."""

from weather_time_mcp.config import DEFAULT_SETTINGS, Settings
from weather_time_mcp.errors import MissingTimezoneError, ValidationError, WeatherTimeMcpError
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

    def get_weather_forecast(
        self,
        location: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        forecast_days: int | None = None,
        include_hourly: bool = False,
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
                forecast_days=forecast_days,
                include_hourly=include_hourly,
            )
        except WeatherTimeMcpError as exc:
            return exc.to_response()

        return {
            "ok": True,
            "provider": "Open-Meteo",
            "resolved_location": resolved_location,
            **forecast,
        }

    def get_current_time(
        self,
        timezone: str | None = None,
        location: str | None = None,
    ) -> dict[str, object]:
        try:
            resolved_location = None
            resolved_timezone = timezone.strip() if timezone else None
            if location:
                candidate = self.resolver.resolve_one(location)
                resolved_location = candidate.to_dict()
                resolved_timezone = candidate.timezone
            if not resolved_timezone:
                raise MissingTimezoneError("provide timezone or a location with timezone metadata")

            current_time = self.time_now.get_current_time(resolved_timezone)
        except WeatherTimeMcpError as exc:
            return exc.to_response()

        return {
            "ok": True,
            "resolved_location": resolved_location,
            **current_time,
        }

    def list_timezones(self) -> dict[str, object]:
        try:
            return {"ok": True, **self.time_now.list_timezones()}
        except WeatherTimeMcpError as exc:
            return exc.to_response()

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
