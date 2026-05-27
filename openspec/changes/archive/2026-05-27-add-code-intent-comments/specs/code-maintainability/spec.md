## ADDED Requirements

### Requirement: Intent Comments for Non-Obvious Behavior

The system SHALL include concise code comments for non-obvious MCP server behavior that exists to preserve tool correctness, LLM reliability, or upstream API compatibility.

#### Scenario: Location-derived timezone precedence is documented

- **WHEN** a maintainer reads the current-time lookup implementation
- **THEN** the code SHALL explain that location-derived timezone data takes precedence over stale or default timezone arguments

#### Scenario: Ambiguous location heuristic is documented

- **WHEN** a maintainer reads the location ambiguity heuristic
- **THEN** the code SHALL explain why clearly dominant results can be auto-selected and uncertain results should return candidates

#### Scenario: Forecast field curation is documented

- **WHEN** a maintainer reads the forecast request construction
- **THEN** the code SHALL explain that curated fields are used to keep the MCP tool assistant-friendly instead of exposing the full upstream API surface

#### Scenario: Timezone path construction is documented

- **WHEN** a maintainer reads the Time.now timezone lookup implementation
- **THEN** the code SHALL explain that IANA timezone names are converted into path segments for the upstream API

### Requirement: Comments Avoid Mechanical Restatement

The system SHALL avoid comments that merely restate simple Python mechanics, assignments, or obvious function names.

#### Scenario: Simple wrapper functions remain uncluttered

- **WHEN** a function only delegates to a clearly named service method
- **THEN** the code SHALL rely on function names and docstrings instead of adding redundant inline comments
