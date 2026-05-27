from weather_time_mcp.models import Location
from weather_time_mcp.service import WeatherTimeService


class FakeOpenMeteo:
    def search_locations(self, query, count=None):  # noqa: ANN001
        return [
            Location(
                id=1,
                name=query,
                latitude=18.52,
                longitude=73.85,
                country="India",
                timezone="Asia/Kolkata",
                population=3_000_000,
            )
        ]

    def get_forecast(self, latitude, longitude, forecast_days=None, include_hourly=False):  # noqa: ANN001
        return {
            "provider": "Open-Meteo",
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "timezone": "Asia/Kolkata",
            "timezone_abbreviation": "IST",
            "utc_offset_seconds": 19800,
            "current": {"temperature_2m": 29.0},
            "current_units": {"temperature_2m": "C"},
            "daily": {"time": ["2026-05-27"]},
            "daily_units": {"temperature_2m_max": "C"},
            "hourly": None,
            "hourly_units": None,
        }


class FakeTimeNow:
    def get_current_time(self, timezone):  # noqa: ANN001
        return {
            "provider": "Time.now",
            "timezone": timezone,
            "datetime": "2026-05-27T12:00:00",
            "utc_offset": "+05:30",
            "timezone_abbreviation": "IST",
            "dst": False,
            "unix_time": 1780000000,
            "raw": {},
        }

    def list_timezones(self):
        return {"provider": "Time.now", "timezones": ["Asia/Kolkata"]}


def make_service():
    return WeatherTimeService(open_meteo=FakeOpenMeteo(), time_now=FakeTimeNow())


def test_current_weather_tool_response_shape():
    result = make_service().get_current_weather(location="Pune")

    assert result["ok"] is True
    assert result["current"]["temperature_2m"] == 29.0
    assert result["resolved_location"]["timezone"] == "Asia/Kolkata"


def test_forecast_tool_response_shape():
    result = make_service().get_weather_forecast(latitude=18.52, longitude=73.85)

    assert result["ok"] is True
    assert result["daily"]["time"] == ["2026-05-27"]


def test_current_time_tool_response_shape():
    result = make_service().get_current_time(location="Pune")

    assert result["ok"] is True
    assert result["timezone"] == "Asia/Kolkata"


def test_list_timezones_tool_response_shape():
    result = make_service().list_timezones()

    assert result == {"ok": True, "provider": "Time.now", "timezones": ["Asia/Kolkata"]}
