"""Client for Open-Meteo geocoding and forecast APIs."""

from typing import Any

import httpx

from weather_time_mcp.config import DEFAULT_SETTINGS, Settings
from weather_time_mcp.errors import UpstreamError, ValidationError
from weather_time_mcp.models import Location


class OpenMeteoClient:
    """Small Open-Meteo API client."""

    def __init__(
        self,
        settings: Settings = DEFAULT_SETTINGS,
        client: httpx.Client | None = None,
    ) -> None:
        self.settings = settings
        self._client = client or httpx.Client(timeout=settings.timeout_seconds)

    def search_locations(self, query: str, count: int | None = None) -> list[Location]:
        """Search Open-Meteo geocoding candidates."""

        normalized_query = query.strip()
        if len(normalized_query) < 2:
            raise ValidationError("location query must contain at least two characters")

        result_count = count or self.settings.default_location_count
        if result_count < 1:
            raise ValidationError("location count must be at least 1")

        payload = self._get_json(
            self.settings.geocoding_url,
            "geocoding",
            params={"name": normalized_query, "count": result_count, "format": "json"},
        )
        return [Location.from_open_meteo(item) for item in payload.get("results", [])]

    def _get_json(
        self,
        url: str,
        operation: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            response = self._client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
        except httpx.TimeoutException as exc:
            raise UpstreamError("Open-Meteo", operation, "request timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise UpstreamError("Open-Meteo", operation, f"HTTP {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise UpstreamError("Open-Meteo", operation, str(exc)) from exc
        except ValueError as exc:
            raise UpstreamError("Open-Meteo", operation, "malformed JSON response") from exc

        if not isinstance(payload, dict):
            raise UpstreamError("Open-Meteo", operation, "unexpected response shape")
        if payload.get("error"):
            reason = str(payload.get("reason") or "upstream error")
            raise UpstreamError("Open-Meteo", operation, reason)
        return payload
