"""Client for Time.now world-time APIs."""

from typing import Any

import httpx

from weather_time_mcp.config import DEFAULT_SETTINGS, Settings
from weather_time_mcp.errors import UpstreamError, ValidationError


class TimeNowClient:
    """Small Time.now API client."""

    def __init__(
        self,
        settings: Settings = DEFAULT_SETTINGS,
        client: httpx.Client | None = None,
    ) -> None:
        self.settings = settings
        self._client = client or httpx.Client(timeout=settings.timeout_seconds)

    def get_current_time(self, timezone: str) -> dict[str, Any]:
        """Fetch current time for an IANA timezone."""

        normalized_timezone = timezone.strip()
        if "/" not in normalized_timezone:
            raise ValidationError("timezone must be an IANA timezone such as Asia/Kolkata")

        path = "/timezone/" + "/".join(part for part in normalized_timezone.split("/") if part)
        payload = self._get_json(path, "timezone lookup")
        return {
            "provider": "Time.now",
            "timezone": normalized_timezone,
            "datetime": payload.get("dateTime") or payload.get("datetime"),
            "date": payload.get("date"),
            "time": payload.get("time"),
            "utc_offset": payload.get("utcOffset") or payload.get("utc_offset"),
            "timezone_abbreviation": payload.get("timeZoneAbbreviation")
            or payload.get("timezone_abbreviation")
            or payload.get("abbreviation"),
            "dst": payload.get("dst") or payload.get("isDst"),
            "unix_time": payload.get("unixTime") or payload.get("unix_time"),
            "raw": payload,
        }

    def list_timezones(self) -> dict[str, Any]:
        """Fetch supported timezone names."""

        payload = self._get_json("/timezone", "timezone listing")
        return {"provider": "Time.now", "timezones": payload}

    def _get_json(self, path: str, operation: str) -> Any:
        url = self.settings.time_now_base_url.rstrip("/") + path
        try:
            response = self._client.get(url)
            response.raise_for_status()
            payload = response.json()
        except httpx.TimeoutException as exc:
            raise UpstreamError("Time.now", operation, "request timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise UpstreamError("Time.now", operation, f"HTTP {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise UpstreamError("Time.now", operation, str(exc)) from exc
        except ValueError as exc:
            raise UpstreamError("Time.now", operation, "malformed JSON response") from exc

        return payload
