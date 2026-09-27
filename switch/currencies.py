from __future__ import annotations

from .exceptions import InvalidCurrencyError

SUPPORTED_CURRENCIES = frozenset(
    {
        "USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "CNY", "HKD",
        "SGD", "INR", "ZAR", "GHS", "NGN", "KES", "EGP", "BRL", "MXN", "ARS",
        "RUB", "TRY", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "ILS", "AED",
        "SAR", "QAR", "KWD", "BHD", "OMR", "JOD", "THB", "MYR", "IDR", "PHP",
        "VND", "KRW", "PKR", "BDT", "LKR", "UAH", "RON", "BGN", "ISK", "CLP",
        "COP", "PEN", "UYU", "XOF", "XAF", "MAD", "TND", "DZD", "ETB", "TZS",
        "UGX", "ZMW", "RWF", "GMD", "BWP", "MUR", "SCR", "JMD", "TTD", "BSD",
        "BBD", "BZD", "GYD", "SRD", "FJD", "PGK", "WST", "TOP", "VUV", "SBD",
        "XPF", "ALL", "MKD", "RSD", "BAM", "MDL", "GEL", "AMD", "AZN", "KZT",
        "UZS", "TJS", "TMT", "KGS", "MNT", "NPR", "BTN", "MMK", "KHR", "LAK",
        "BND", "TWD", "MOP", "AFN", "IQD", "IRR", "LBP", "LYD", "SDG", "SOS",
        "SYP", "YER", "CUP", "HTG", "HNL", "GTQ", "NIO", "CRC", "PAB", "DOP",
        "PYG", "BOB", "VES", "ANG", "AWG", "XCD", "KYD", "BMD",
    }
)


def validate_currency_code(code: object) -> str:
    if not isinstance(code, str):
        raise InvalidCurrencyError(code)
    normalized = code.strip().upper()
    if len(normalized) != 3 or normalized not in SUPPORTED_CURRENCIES:
        raise InvalidCurrencyError(code)
    return normalized
