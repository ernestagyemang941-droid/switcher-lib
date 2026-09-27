from __future__ import annotations

from .converter import CurrencyConverter
from .currencies import SUPPORTED_CURRENCIES
from .exceptions import (
    CurrencyConverterError,
    InvalidAmountError,
    InvalidCurrencyError,
    NetworkError,
    ProviderError,
    ProviderResponseError,
    RateNotFoundError,
)
from .providers.base import ExchangeRateProvider

__version__ = "0.1.0"

__all__ = [
    "CurrencyConverter",
    "SUPPORTED_CURRENCIES",
    "CurrencyConverterError",
    "InvalidAmountError",
    "InvalidCurrencyError",
    "NetworkError",
    "ProviderError",
    "ProviderResponseError",
    "RateNotFoundError",
    "ExchangeRateProvider",
]
