"""Domain errors for upstream API and validation failures."""


class WeatherTimeMcpError(Exception):
    """Base exception for server-domain failures."""

    code = "weather_time_mcp_error"

    def to_response(self) -> dict[str, object]:
        return {"ok": False, "error": self.code, "message": str(self)}


class ValidationError(WeatherTimeMcpError):
    """Raised when tool arguments are invalid."""

    code = "validation_error"


class UpstreamError(WeatherTimeMcpError):
    """Raised when an upstream provider fails."""

    code = "upstream_error"

    def __init__(self, provider: str, operation: str, reason: str) -> None:
        super().__init__(f"{provider} {operation} failed: {reason}")
        self.provider = provider
        self.operation = operation
        self.reason = reason

    def to_response(self) -> dict[str, object]:
        return {
            "ok": False,
            "error": self.code,
            "provider": self.provider,
            "operation": self.operation,
            "reason": self.reason,
        }


class AmbiguousLocationError(WeatherTimeMcpError):
    """Raised when a location has multiple plausible matches."""

    code = "ambiguous_location"

    def __init__(self, query: str, candidates: list[dict[str, object]]) -> None:
        super().__init__(f"Location '{query}' is ambiguous")
        self.query = query
        self.candidates = candidates

    def to_response(self) -> dict[str, object]:
        return {
            "ok": False,
            "error": self.code,
            "message": str(self),
            "query": self.query,
            "candidates": self.candidates,
        }
