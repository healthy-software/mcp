import pytest

from weather_time_mcp.errors import ValidationError
from weather_time_mcp.open_meteo import OpenMeteoClient
from weather_time_mcp.service import WeatherTimeService


class UnusedOpenMeteo:
    def search_locations(self, query, count=None):  # noqa: ANN001
        raise AssertionError("should not geocode")

    def get_forecast(self, **kwargs):  # noqa: ANN003
        raise AssertionError("should not fetch forecast")


def test_forecast_days_must_be_in_range():
    client = OpenMeteoClient()

    with pytest.raises(ValidationError, match="forecast_days"):
        client.get_forecast(latitude=1.0, longitude=2.0, forecast_days=17)


def test_current_weather_requires_location_or_coordinates():
    service = WeatherTimeService(open_meteo=UnusedOpenMeteo())

    result = service.get_current_weather()

    assert result["ok"] is False
    assert result["error"] == "validation_error"
