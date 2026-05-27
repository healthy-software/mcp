## Why

Several parts of the weather/time MCP server encode product intent that is not obvious from the mechanics alone, especially location-vs-timezone precedence and ambiguity handling. Targeted comments will make those decisions easier to preserve while avoiding noisy line-by-line explanation.

## What Changes

- Add concise intent comments near non-obvious policy decisions.
- Clarify that a freshly resolved location timezone takes precedence over stale/default timezone arguments.
- Clarify the location ambiguity heuristic.
- Clarify why forecast fields are curated instead of exposing the full upstream Open-Meteo surface.
- Clarify Time.now timezone path construction from IANA timezone segments.
- No runtime behavior changes.

## Capabilities

### New Capabilities

- `code-maintainability`: Defines maintainability expectations for targeted intent comments in the MCP server code.

### Modified Capabilities

None.

## Impact

- Affects comments only in Python source files.
- No API, MCP tool schema, dependency, Docker, or runtime behavior changes.
- Tests should continue to pass unchanged.
