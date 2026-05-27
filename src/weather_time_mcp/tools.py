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
    def list_timezones() -> dict[str, object]:
        """List IANA timezone names supported by the time provider."""

        raise NotImplementedError("list_timezones is implemented in a later task")
