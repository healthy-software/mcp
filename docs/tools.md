# Tool Reference

## `search_locations`

Search Open-Meteo geocoding candidates for a human-readable place name.

Parameters:

- `query`: place name to search.
- `count`: optional maximum number of candidates.

Returns:

- `ok`
- `provider`
- `query`
- `locations`

## `get_current_weather`

Get current weather for a location string or coordinates. Location strings are resolved through Open-Meteo geocoding before weather data is requested.

Parameters:

- `location`: optional place name.
- `latitude`: optional coordinate.
- `longitude`: optional coordinate.

Returns:

- `ok`
- `provider`
- `resolved_location`
- `coordinates`
- `timezone`
- `current`
- `current_units`

## `get_weather_forecast`

Get a daily weather forecast, with optional hourly data.

Parameters:

- `location`: optional place name.
- `latitude`: optional coordinate.
- `longitude`: optional coordinate.
- `forecast_days`: optional number of days, from 1 to 16.
- `include_hourly`: optional boolean.

Returns:

- `ok`
- `provider`
- `resolved_location`
- `coordinates`
- `timezone`
- `current`
- `current_units`
- `daily`
- `daily_units`
- `hourly`
- `hourly_units`

## `get_current_time`

Get current time from an IANA timezone or geocoded location.

Parameters:

- `timezone`: optional IANA timezone such as `Asia/Kolkata`.
- `location`: optional place name.

Returns:

- `ok`
- `provider`
- `resolved_location`
- `timezone`
- `datetime`
- `date`
- `time`
- `utc_offset`
- `timezone_abbreviation`
- `dst`
- `unix_time`

## `list_timezones`

List timezone names supplied by Time.now.

Parameters: none.

Returns:

- `ok`
- `provider`
- `timezones`
