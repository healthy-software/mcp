## 1. Project Setup

- [x] 1.1 Add Python project metadata and dependencies for FastMCP, HTTP requests, and testing
- [x] 1.2 Create the server package structure and FastMCP entry point
- [x] 1.3 Add configuration constants for upstream base URLs, request timeouts, and default forecast options

## 2. Upstream API Clients

- [x] 2.1 Implement the Open-Meteo geocoding client with validation and timeout handling
- [x] 2.2 Implement the Open-Meteo forecast client with curated current, hourly, and daily fields
- [x] 2.3 Implement the Time.now client for timezone lookup and timezone listing
- [x] 2.4 Normalize upstream errors into provider-specific error objects

## 3. Resolver and Tool Behavior

- [x] 3.1 Implement location resolution from text to geocoding candidates
- [x] 3.2 Implement ambiguity detection that returns candidates instead of silently selecting uncertain matches
- [x] 3.3 Implement `search_locations`
- [x] 3.4 Implement `get_current_weather`
- [x] 3.5 Implement `get_weather_forecast`
- [x] 3.6 Implement `get_current_time`
- [x] 3.7 Implement `list_timezones`

## 4. Tests and Validation

- [x] 4.1 Add unit tests for argument validation and forecast duration bounds
- [x] 4.2 Add unit tests for location resolution and ambiguous location responses
- [x] 4.3 Add unit tests for upstream error and timeout handling
- [x] 4.4 Add MCP tool tests or integration tests with mocked upstream APIs
- [x] 4.5 Run OpenSpec validation for `add-weather-time-mcp-server`

## 5. Documentation

- [ ] 5.1 Document server setup and MCP client configuration
- [ ] 5.2 Document available tools, parameters, and example prompts
- [ ] 5.3 Add Open-Meteo and Time.now attribution
