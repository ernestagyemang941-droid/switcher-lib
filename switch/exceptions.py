from __future__ import annotations


class CurrencyConverterError(Exception):
    pass


class InvalidCurrencyError(CurrencyConverterError):
    def __init__(self, currency_code: object) -> None:
        super().__init__(f"Invalid or unsupported currency code: {currency_code!r}")
        self.currency_code = currency_code


class InvalidAmountError(CurrencyConverterError):
    def __init__(self, amount: object) -> None:
        super().__init__(f"Invalid amount for conversion: {amount!r}")
        self.amount = amount


class ProviderError(CurrencyConverterError):
    pass


class NetworkError(ProviderError):
    pass


class ProviderResponseError(ProviderError):
    pass


class RateNotFoundError(ProviderError):
    def __init__(self, from_currency: str, to_currency: str) -> None:
        super().__init__(f"Exchange rate not available for {from_currency} -> {to_currency}")
        self.from_currency = from_currency
        self.to_currency = to_currency
