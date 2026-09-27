from __future__ import annotations

import pytest

from switch.currencies import validate_currency_code
from switch.exceptions import InvalidCurrencyError


def test_validate_currency_code_normalizes_case_and_whitespace() -> None:
    assert validate_currency_code(" usd ") == "USD"


def test_validate_currency_code_accepts_supported_code() -> None:
    assert validate_currency_code("GHS") == "GHS"


def test_validate_currency_code_rejects_unknown_code() -> None:
    with pytest.raises(InvalidCurrencyError):
        validate_currency_code("XXX")


def test_validate_currency_code_rejects_wrong_length() -> None:
    with pytest.raises(InvalidCurrencyError):
        validate_currency_code("US")


def test_validate_currency_code_rejects_non_string() -> None:
    with pytest.raises(InvalidCurrencyError):
        validate_currency_code(123)
