## Context

The server will let an LLM answer questions such as "What is the current weather in Pune?" or "What time is it in Japan?" through MCP tools. Users will often provide place names rather than coordinates or timezone identifiers, so the server needs a resolver layer between assistant-facing tools and raw upstream APIs.

The implementation will use Python and FastMCP. Open-Meteo provides geocoding and weather forecast APIs without an API key. Time.now provides world-time data and timezone listing without an API key, with attribution requested by the provider.

## Goals / Non-Goals

**Goals:**

- Provide assistant-friendly MCP tools for current weather, forecasts, location search, timezone listing, and current time.
- Accept human-readable locations for weather tools and resolve them to coordinates through Open-Meteo geocoding.
- Accept locations or IANA timezones for time lookup, using geocoding-derived timezone data when a location is provided.
- Return concise normalized data suitable for LLM use while preserving key raw metadata such as resolved location, coordinates, timezone, units, and upstream timestamps.
- Fail predictably for ambiguous locations, invalid arguments, upstream API errors, and network failures.

**Non-Goals:**

- Do not implement a frontend or persistent user profile store.
- Do not infer the user's physical location unless a client explicitly passes a location, coordinates, timezone, or IP-based lookup option in a future change.
- Do not wrap every Open-Meteo endpoint in the first version.
- Do not provide severe-weather alerts unless a supported upstream API and requirement are added later.

## Decisions

### Use FastMCP for the MCP server

FastMCP keeps tool definitions close to typed Python functions and is sufficient for a compact API-wrapper server. The alternative is using a lower-level MCP SDK directly, which gives more control but adds boilerplate before the domain behavior is proven.

### Expose assistant-facing tools rather than raw upstream endpoints

Tools will model user intent:

- `get_current_weather`
- `get_weather_forecast`
- `search_locations`
- `get_current_time`
- `list_timezones`

This keeps the LLM from needing to know Open-Meteo endpoint structure for common questions. Raw API coverage can be expanded later if a need appears.

### Treat geocoding as a resolver behind weather tools

When a weather tool receives a location string, the server resolves it through Open-Meteo geocoding and uses the selected latitude and longitude for forecast calls. If multiple plausible matches are returned and there is no clearly selected result, the server returns candidate locations so the LLM can ask the user to clarify.

### Use explicit, bounded forecast options

The first version will expose forecast days and a curated set of current, hourly, and daily fields rather than arbitrary upstream parameter dictionaries. This makes tool schemas easier for LLMs to call correctly and reduces invalid upstream requests.

### Use Time.now timezone endpoints for current time

`get_current_time` will accept an IANA timezone directly. If a location string is provided, the server will geocode it and use the returned timezone. Country names alone can be ambiguous; where a country has multiple timezones, the tool should return candidates or require a city/timezone.

## Risks / Trade-offs

- Ambiguous place names can produce incorrect answers if auto-selected -> return candidates when confidence is unclear and include resolved location metadata in successful responses.
- Upstream APIs can be slow or unavailable -> set request timeouts and return structured error details.
- Free API terms can change -> keep base URLs and attribution documented, and avoid hiding upstream provider identity.
- Weather variable names can become too broad for reliable tool use -> start with curated defaults and add options only when needed.
- Country-level time lookup can be imprecise -> prefer IANA timezone or city-level location for current-time queries.

## Migration Plan

This is a new capability with no existing behavior to migrate. Rollback is removal of the new server entry point, dependencies, and documentation.

## Open Questions

- Should the server use synchronous HTTP requests for simplicity or async HTTP for better concurrency?
- Should weather tools return raw upstream payloads, normalized summaries, or both?
- Should IP-based time lookup from Time.now be exposed now, or deferred because of privacy expectations?
