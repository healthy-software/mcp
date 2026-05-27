# Weather Time MCP

Python FastMCP server that exposes Open-Meteo weather/geocoding data and Time.now world-time data to MCP clients.

## Setup

Create a local Python environment and install the package:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[test]"
```

Run tests:

```bash
.venv/bin/python -m pytest
```

Start the MCP server:

```bash
.venv/bin/weather-time-mcp
```

## MCP Client Configuration

Configure an MCP client to launch the server command from this repository:

```json
{
  "mcpServers": {
    "weather-time": {
      "command": "/home/agent/projects/mcp/.venv/bin/weather-time-mcp"
    }
  }
}
```

If the project is installed in a different location, update the command path to that environment's `weather-time-mcp` script.

## Tools

### `search_locations`

Searches Open-Meteo geocoding candidates for a place name.

Parameters:

- `query`: place name to search
- `count`: optional maximum number of candidates

Example prompt:

```text
Find location candidates for Springfield.
```

### `get_current_weather`

Gets current weather for a location string or coordinates. When `location` is provided, the server geocodes it before requesting weather data.

Parameters:

- `location`: optional place name
- `latitude`: optional coordinate
- `longitude`: optional coordinate

Example prompt:

```text
What is the current weather in Pune?
```

### `get_weather_forecast`

Gets a weather forecast for a location string or coordinates.

Parameters:

- `location`: optional place name
- `latitude`: optional coordinate
- `longitude`: optional coordinate
- `forecast_days`: optional number of days, from 1 to 16
- `include_hourly`: optional boolean for hourly data

Example prompt:

```text
Give me a 3 day forecast for Tokyo.
```

### `get_current_time`

Gets current local time for an IANA timezone or for a geocoded location.

Parameters:

- `timezone`: optional IANA timezone such as `Asia/Kolkata`
- `location`: optional place name

Example prompt:

```text
What time is it in Japan?
```

### `list_timezones`

Lists timezone names from Time.now.

Example prompt:

```text
List supported timezones.
```

## Attribution

Weather and geocoding data comes from [Open-Meteo](https://open-meteo.com/).

World-time data comes from [Time.now](https://time.now/).
