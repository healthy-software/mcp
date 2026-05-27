## Why

LLMs need a reliable way to answer weather and local-time questions for places named by users without requiring users to provide coordinates or IANA timezone identifiers. A small MCP server can expose these capabilities through typed tools backed by free public APIs.

## What Changes

- Add a Python MCP server built with FastMCP.
- Add weather tools backed by Open-Meteo forecast data.
- Resolve human-readable weather locations through Open-Meteo geocoding before calling forecast APIs.
- Add world-time tools backed by the Time.now World Time API.
- Handle ambiguous locations by returning candidates instead of silently choosing an uncertain match.
- Normalize upstream API errors into structured MCP tool errors or responses.
- Include upstream attribution requirements in project documentation.

## Capabilities

### New Capabilities

- `weather-time-mcp-server`: Exposes MCP tools for location-based weather forecasts, current weather, location search, timezone discovery, and current time lookup.

### Modified Capabilities

None.

## Impact

- Adds Python and FastMCP as implementation dependencies.
- Adds outbound HTTPS calls to Open-Meteo geocoding, Open-Meteo forecast, and Time.now World Time APIs.
- Adds MCP tool schemas and tests for location resolution, weather retrieval, time retrieval, ambiguity handling, and API error handling.
