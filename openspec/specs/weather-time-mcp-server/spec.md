# Weather Time MCP Server

## Purpose

Provide MCP tools that let LLMs answer weather, forecast, location-search, and world-time questions using Open-Meteo and Time.now.

## Requirements

### Requirement: FastMCP Server Entry Point

The system SHALL provide a Python FastMCP server that registers weather and time tools for use by MCP clients.

#### Scenario: Server starts

- **WHEN** the MCP server process is started
- **THEN** the server SHALL expose its registered tools through the FastMCP runtime

### Requirement: Location Search

The system SHALL provide a tool that searches human-readable place names using Open-Meteo geocoding and returns candidate locations.

#### Scenario: Location candidates are found

- **WHEN** the LLM calls the location search tool with a valid query
- **THEN** the system SHALL return candidate locations including name, country, administrative region when available, latitude, longitude, and timezone

#### Scenario: Location query is too vague

- **WHEN** the LLM calls the location search tool with a missing or insufficient query
- **THEN** the system SHALL return a validation error without calling the upstream API

### Requirement: Current Weather by Location

The system SHALL provide a current-weather tool that accepts either coordinates or a human-readable location.

#### Scenario: Current weather for named location

- **WHEN** the LLM requests current weather with a location string
- **THEN** the system SHALL resolve the location through Open-Meteo geocoding before requesting weather data
- **AND** the system SHALL return current weather data with the resolved location metadata

#### Scenario: Current weather for coordinates

- **WHEN** the LLM requests current weather with latitude and longitude
- **THEN** the system SHALL request weather data without performing geocoding

### Requirement: Weather Forecast by Location

The system SHALL provide a forecast tool that returns weather forecast data for a resolved location or coordinates.

#### Scenario: Forecast for named location

- **WHEN** the LLM requests a forecast with a location string and forecast duration
- **THEN** the system SHALL resolve the location through Open-Meteo geocoding
- **AND** the system SHALL request forecast data for the resolved latitude and longitude

#### Scenario: Forecast duration is outside allowed range

- **WHEN** the LLM requests a forecast duration outside the supported Open-Meteo range
- **THEN** the system SHALL return a validation error before calling the forecast API

### Requirement: Ambiguous Location Handling

The system SHALL avoid silently selecting a location when the geocoding response contains multiple plausible matches and no explicit coordinates or selected candidate is provided.

#### Scenario: Ambiguous named location

- **WHEN** a weather or time tool receives a location string that resolves to multiple plausible places
- **THEN** the system SHALL return candidate locations for clarification instead of returning weather or time for an arbitrary candidate

### Requirement: Current Time Lookup

The system SHALL provide a tool that returns the current time for an IANA timezone or a resolvable location.

#### Scenario: Time for timezone

- **WHEN** the LLM requests current time with a valid IANA timezone
- **THEN** the system SHALL call the Time.now timezone endpoint and return the local datetime, UTC offset, timezone abbreviation, DST status, and Unix time

#### Scenario: Time for named location

- **WHEN** the LLM requests current time with a location string
- **THEN** the system SHALL resolve the location through Open-Meteo geocoding
- **AND** the system SHALL call Time.now using the resolved IANA timezone

### Requirement: Timezone Listing

The system SHALL provide a tool that lists valid IANA timezone names from Time.now.

#### Scenario: Timezones requested

- **WHEN** the LLM requests available timezones
- **THEN** the system SHALL return the timezone names supplied by Time.now

### Requirement: Upstream Error Handling

The system SHALL convert upstream validation errors, HTTP failures, timeouts, and malformed responses into structured tool errors or structured error responses.

#### Scenario: Upstream API returns an error

- **WHEN** an upstream API returns an error response
- **THEN** the system SHALL include the provider name, operation, and error reason in the tool response or raised tool error

#### Scenario: Upstream API times out

- **WHEN** an upstream API request exceeds the configured timeout
- **THEN** the system SHALL return a timeout error that identifies the provider and operation

### Requirement: Provider Attribution

The project documentation SHALL identify Open-Meteo and Time.now as upstream data providers and include any required attribution text or links.

#### Scenario: Documentation is reviewed

- **WHEN** a developer reads the project documentation
- **THEN** the documentation SHALL state that weather/geocoding data comes from Open-Meteo and world-time data comes from Time.now
