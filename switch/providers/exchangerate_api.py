from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

import requests

from ..exceptions import NetworkError, ProviderResponseError, RateNotFoundError
from .base import ExchangeRateProvider

DEFAULT_BASE_URL = "https://open.er-api.com/v6/latest"


class ExchangeRateAPIProvider(ExchangeRateProvider):
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def get_rate(self, from_currency: str, to_currency: str) -> Decimal:
        payload = self._fetch(from_currency)
        rates = payload.get("rates")
        if not isinstance(rates, dict):
            raise ProviderResponseError("Exchange rate provider response is missing rates")
        rate = rates.get(to_currency)
        if rate is None:
            raise RateNotFoundError(from_currency, to_currency)
        try:
            return Decimal(str(rate))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ProviderResponseError(f"Malformed rate value for {to_currency}") from exc

    def _fetch(self, base_currency: str) -> dict[str, Any]:
        url = f"{self._base_url}/{base_currency}"
        try:
            response = requests.get(url, timeout=self._timeout)
        except requests.Timeout as exc:
            raise NetworkError("Request to exchange rate provider timed out") from exc
        except requests.RequestException as exc:
            raise NetworkError(f"Failed to reach exchange rate provider: {exc}") from exc

        if response.status_code != 200:
            raise ProviderResponseError(
                f"Exchange rate provider returned status {response.status_code}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise ProviderResponseError("Exchange rate provider returned invalid JSON") from exc

        if not isinstance(data, dict) or data.get("result") != "success":
            raise ProviderResponseError("Exchange rate provider reported an error")

        return data
