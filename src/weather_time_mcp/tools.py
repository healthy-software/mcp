"""MCP tool registration."""

from fastmcp import FastMCP

from weather_time_mcp.service import WeatherTimeService


def register_tools(server: FastMCP) -> None:
    """Register weather and time tools with a FastMCP server."""

    service = WeatherTimeService()

    @server.tool()
    def search_locations(query: str, count: int | None = None) -> dict[str, object]:
        """Search for candidate locations by place name."""

        return service.search_locations(query, count=count)

    @server.tool()
    def get_current_weather(
        location: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict[str, object]:
        """Get current weather for a location name or coordinates."""

        return service.get_current_weather(location=location, latitude=latitude, longitude=longitude)

    @server.tool()
    def get_weather_forecast(
        location: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        forecast_days: int | None = None,
        include_hourly: bool = False,
    ) -> dict[str, object]:
        """Get a weather forecast for a location name or coordinates."""

        return service.get_weather_forecast(
            location=location,
            latitude=latitude,
            longitude=longitude,
            forecast_days=forecast_days,
            include_hourly=include_hourly,
        )

    @server.tool()
    def list_timezones() -> dict[str, object]:
        """List IANA timezone names supported by the time provider."""

        raise NotImplementedError("list_timezones is implemented in a later task")
