"""MCP tool registration."""

from fastmcp import FastMCP


def register_tools(server: FastMCP) -> None:
    """Register weather and time tools with a FastMCP server."""

    @server.tool()
    def list_timezones() -> dict[str, object]:
        """List IANA timezone names supported by the time provider."""

        raise NotImplementedError("list_timezones is implemented in a later task")
