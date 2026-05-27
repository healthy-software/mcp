"""FastMCP server entry point for weather and time tools."""

from fastmcp import FastMCP

from weather_time_mcp.tools import register_tools


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""

    server = FastMCP("weather-time-mcp")
    register_tools(server)
    return server


def main() -> None:
    """Run the MCP server."""

    create_server().run()


if __name__ == "__main__":
    main()
