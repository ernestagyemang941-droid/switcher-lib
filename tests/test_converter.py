from __future__ import annotations

from decimal import Decimal

import pytest

from switch import CurrencyConverter
from switch.exceptions import (
    InvalidAmountError,
    InvalidCurrencyError,
    RateNotFoundError,
)
from switch.providers.base import ExchangeRateProvider


class FakeProvider(ExchangeRateProvider):
    def __init__(self, rates: dict[tuple[str, str], Decimal]) -> None:
        self._rates = rates

    def get_rate(self, from_currency: str, to_currency: str) -> Decimal:
        key = (from_currency, to_currency)
        if key not in self._rates:
            raise RateNotFoundError(from_currency, to_currency)
        return self._rates[key]


@pytest.fixture
def converter() -> CurrencyConverter:
    provider = FakeProvider({("USD", "GHS"): Decimal("15.5")})
    return CurrencyConverter(provider=provider)


def test_convert_returns_expected_amount(converter: CurrencyConverter) -> None:
    assert converter.convert(100, "USD", "GHS") == pytest.approx(1550.0)


def test_convert_accepts_case_insensitive_codes(converter: CurrencyConverter) -> None:
    assert converter.convert(10, "usd", "ghs") == pytest.approx(155.0)


def test_convert_same_currency_skips_provider(converter: CurrencyConverter) -> None:
    assert converter.convert(42, "USD", "USD") == 42.0


def test_convert_zero_amount_is_valid(converter: CurrencyConverter) -> None:
    assert converter.convert(0, "USD", "GHS") == 0.0


def test_convert_rejects_negative_amount(converter: CurrencyConverter) -> None:
    with pytest.raises(InvalidAmountError):
        converter.convert(-5, "USD", "GHS")


def test_convert_rejects_non_numeric_amount(converter: CurrencyConverter) -> None:
    with pytest.raises(InvalidAmountError):
        converter.convert("not-a-number", "USD", "GHS")


def test_convert_rejects_nan_amount(converter: CurrencyConverter) -> None:
    with pytest.raises(InvalidAmountError):
        converter.convert(float("nan"), "USD", "GHS")


def test_convert_rejects_invalid_currency_code(converter: CurrencyConverter) -> None:
    with pytest.raises(InvalidCurrencyError):
        converter.convert(100, "USD", "XXX")


def test_convert_propagates_rate_not_found(converter: CurrencyConverter) -> None:
    with pytest.raises(RateNotFoundError):
        converter.convert(100, "GHS", "EUR")


def test_get_exchange_rate_returns_provider_rate(converter: CurrencyConverter) -> None:
    assert converter.get_exchange_rate("USD", "GHS") == pytest.approx(15.5)


def test_get_exchange_rate_same_currency_returns_one(converter: CurrencyConverter) -> None:
    assert converter.get_exchange_rate("EUR", "EUR") == 1.0
