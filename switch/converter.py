from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional, Union

from .currencies import validate_currency_code
from .exceptions import InvalidAmountError
from .providers.base import ExchangeRateProvider
from .providers.exchangerate_api import ExchangeRateAPIProvider

Number = Union[int, float, str, Decimal]


class CurrencyConverter:
    def __init__(
        self,
        provider: Optional[ExchangeRateProvider] = None,
        timeout: float = 10.0,
    ) -> None:
        self._provider = provider or ExchangeRateAPIProvider(timeout=timeout)

    def convert(self, amount: Number, from_currency: str, to_currency: str) -> float:
        decimal_amount = self._to_decimal(amount)
        from_code = validate_currency_code(from_currency)
        to_code = validate_currency_code(to_currency)
        if from_code == to_code:
            return float(decimal_amount)
        rate = self._provider.get_rate(from_code, to_code)
        return float(decimal_amount * rate)

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        from_code = validate_currency_code(from_currency)
        to_code = validate_currency_code(to_currency)
        if from_code == to_code:
            return 1.0
        return float(self._provider.get_rate(from_code, to_code))

    @staticmethod
    def _to_decimal(amount: Number) -> Decimal:
        if isinstance(amount, bool):
            raise InvalidAmountError(amount)
        try:
            decimal_amount = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise InvalidAmountError(amount) from exc
        if not decimal_amount.is_finite() or decimal_amount < 0:
            raise InvalidAmountError(amount)
        return decimal_amount
