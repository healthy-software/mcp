"""Configuration defaults for upstream APIs."""

from dataclasses import dataclass, field

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIME_NOW_BASE_URL = "https://time.now/developer/api"

REQUEST_TIMEOUT_SECONDS = 10.0
DEFAULT_LOCATION_COUNT = 5
DEFAULT_FORECAST_DAYS = 7
MAX_FORECAST_DAYS = 16

CURRENT_WEATHER_FIELDS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "is_day",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
]

HOURLY_FORECAST_FIELDS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation_probability",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
]

DAILY_FORECAST_FIELDS = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
]


@dataclass(frozen=True)
class Settings:
    """Runtime settings shared by clients and tools."""

    geocoding_url: str = OPEN_METEO_GEOCODING_URL
    forecast_url: str = OPEN_METEO_FORECAST_URL
    time_now_base_url: str = TIME_NOW_BASE_URL
    timeout_seconds: float = REQUEST_TIMEOUT_SECONDS
    default_location_count: int = DEFAULT_LOCATION_COUNT
    default_forecast_days: int = DEFAULT_FORECAST_DAYS
    max_forecast_days: int = MAX_FORECAST_DAYS
    current_weather_fields: list[str] = field(default_factory=lambda: CURRENT_WEATHER_FIELDS.copy())
    hourly_forecast_fields: list[str] = field(default_factory=lambda: HOURLY_FORECAST_FIELDS.copy())
    daily_forecast_fields: list[str] = field(default_factory=lambda: DAILY_FORECAST_FIELDS.copy())


DEFAULT_SETTINGS = Settings()
