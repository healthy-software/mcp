import httpx
import pytest

from weather_time_mcp.errors import UpstreamError
from weather_time_mcp.open_meteo import OpenMeteoClient
from weather_time_mcp.time_now import TimeNowClient


def test_open_meteo_timeout_is_normalized():
    def handler(request):  # noqa: ANN001
        raise httpx.TimeoutException("slow", request=request)

    client = OpenMeteoClient(client=httpx.Client(transport=httpx.MockTransport(handler)))

    with pytest.raises(UpstreamError) as exc_info:
        client.search_locations("Pune")

    assert exc_info.value.provider == "Open-Meteo"
    assert exc_info.value.reason == "request timed out"


def test_open_meteo_upstream_error_payload_is_normalized():
    def handler(request):  # noqa: ANN001
        return httpx.Response(200, json={"error": True, "reason": "bad request"})

    client = OpenMeteoClient(client=httpx.Client(transport=httpx.MockTransport(handler)))

    with pytest.raises(UpstreamError) as exc_info:
        client.search_locations("Pune")

    assert exc_info.value.reason == "bad request"


def test_time_now_http_error_is_normalized():
    def handler(request):  # noqa: ANN001
        return httpx.Response(500, json={"error": "boom"})

    client = TimeNowClient(client=httpx.Client(transport=httpx.MockTransport(handler)))

    with pytest.raises(UpstreamError) as exc_info:
        client.get_current_time("Asia/Kolkata")

    assert exc_info.value.provider == "Time.now"
    assert exc_info.value.reason == "HTTP 500"
