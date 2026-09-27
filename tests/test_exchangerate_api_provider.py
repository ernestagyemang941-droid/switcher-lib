from __future__ import annotations

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
import requests

from switch.exceptions import (
    NetworkError,
    ProviderResponseError,
    RateNotFoundError,
)
from switch.providers.exchangerate_api import ExchangeRateAPIProvider


def _mock_response(status_code: int = 200, json_data: dict | None = None) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data or {}
    return response


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_returns_decimal_on_success(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(
        200, {"result": "success", "rates": {"GHS": "15.5"}}
    )
    provider = ExchangeRateAPIProvider()
    assert provider.get_rate("USD", "GHS") == Decimal("15.5")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_uses_configured_timeout(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(
        200, {"result": "success", "rates": {"GHS": "15.5"}}
    )
    provider = ExchangeRateAPIProvider(timeout=3.5)
    provider.get_rate("USD", "GHS")
    _, kwargs = mock_get.call_args
    assert kwargs["timeout"] == 3.5


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_rate_not_found_for_missing_currency(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(
        200, {"result": "success", "rates": {"EUR": "0.9"}}
    )
    provider = ExchangeRateAPIProvider()
    with pytest.raises(RateNotFoundError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_network_error_on_timeout(mock_get: Mock) -> None:
    mock_get.side_effect = requests.Timeout()
    provider = ExchangeRateAPIProvider()
    with pytest.raises(NetworkError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_network_error_on_connection_failure(mock_get: Mock) -> None:
    mock_get.side_effect = requests.ConnectionError()
    provider = ExchangeRateAPIProvider()
    with pytest.raises(NetworkError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_response_error_on_bad_status(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(500, {})
    provider = ExchangeRateAPIProvider()
    with pytest.raises(ProviderResponseError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_response_error_on_invalid_json(mock_get: Mock) -> None:
    response = _mock_response(200)
    response.json.side_effect = ValueError("bad json")
    mock_get.return_value = response
    provider = ExchangeRateAPIProvider()
    with pytest.raises(ProviderResponseError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_response_error_when_result_is_not_success(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(200, {"result": "error"})
    provider = ExchangeRateAPIProvider()
    with pytest.raises(ProviderResponseError):
        provider.get_rate("USD", "GHS")


@patch("switch.providers.exchangerate_api.requests.get")
def test_get_rate_raises_response_error_on_malformed_rate(mock_get: Mock) -> None:
    mock_get.return_value = _mock_response(
        200, {"result": "success", "rates": {"GHS": "not-a-number"}}
    )
    provider = ExchangeRateAPIProvider()
    with pytest.raises(ProviderResponseError):
        provider.get_rate("USD", "GHS")
