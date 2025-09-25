import re
from datetime import datetime
from typing import Any, Optional

import requests

from ..config import Config
from ..exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    ValidationException,
)
from ..interfaces.base import BaseDataService


class ForexService(BaseDataService):
    """Foreign exchange data service based on free exchange rate API"""

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        # exchangerate-api.com - Free API (1500 requests/month limit)
        self.base_url = "https://api.exchangerate-api.com/v4/latest"

    def get_data(self, base_currency: str = "USD", **kwargs) -> dict[str, Any]:
        """
        Retrieves exchange rate data.

        Args:
            base_currency: Base currency (e.g., "USD", "KRW", "EUR")

        Returns:
            Dict: Exchange rate data
        """
        if not self.validate_symbol(base_currency):
            raise ValidationException(
                f"Invalid currency code: {base_currency}", field="base_currency"
            )

        formatted_currency = self._format_symbol(base_currency)
        url = f"{self.base_url}/{formatted_currency}"

        try:
            response = requests.get(url, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if "rates" not in data:
                raise DataNotFoundException(
                    f"No exchange rate data found for: {base_currency}"
                )

            return {
                "base": data.get("base"),
                "date": data.get("date"),
                "rates": data.get("rates"),
                "timestamp": datetime.now().isoformat(),
            }

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch forex data for {base_currency}: {str(e)}",
                original_error=e,
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def get_rate(self, from_currency: str, to_currency: str) -> dict[str, Any]:
        """
        Retrieves exchange rate for specific currency pair.

        Args:
            from_currency: Base currency
            to_currency: Target currency

        Returns:
            Dict: Exchange rate information
        """
        if not self.validate_symbol(from_currency):
            raise ValidationException(
                f"Invalid currency code: {from_currency}", field="from_currency"
            )

        if not self.validate_symbol(to_currency):
            raise ValidationException(
                f"Invalid currency code: {to_currency}", field="to_currency"
            )

        data = self.get_data(from_currency)

        to_currency_upper = to_currency.upper()
        if to_currency_upper not in data["rates"]:
            raise DataNotFoundException(
                f"Exchange rate not found for {from_currency} to {to_currency}"
            )

        return {
            "from": from_currency.upper(),
            "to": to_currency_upper,
            "rate": data["rates"][to_currency_upper],
            "date": data["date"],
            "timestamp": data["timestamp"],
        }

    def get_major_pairs(self) -> dict[str, Any]:
        """
        Retrieves exchange rates for major currency pairs.

        Returns:
            Dict: Major currency pairs exchange rates
        """
        major_currencies = ["EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "KRW"]

        try:
            usd_data = self.get_data("USD")

            major_rates = {}
            for currency in major_currencies:
                if currency in usd_data["rates"]:
                    major_rates[f"USD/{currency}"] = usd_data["rates"][currency]

            return {
                "base": "USD",
                "rates": major_rates,
                "date": usd_data["date"],
                "timestamp": usd_data["timestamp"],
            }

        except Exception as e:
            raise APIException(f"Failed to fetch major currency pairs: {str(e)}") from e

    def get_supported_currencies(self) -> list[str]:
        """
        Retrieves list of supported currencies.

        Returns:
            List[str]: List of supported currency codes
        """
        try:
            data = self.get_data("USD")
            return list(data["rates"].keys()) + ["USD"]
        except Exception:
            # Return default major currencies list
            return [
                "USD",
                "EUR",
                "GBP",
                "JPY",
                "CHF",
                "CAD",
                "AUD",
                "NZD",
                "KRW",
                "CNY",
                "INR",
                "BRL",
                "RUB",
                "ZAR",
                "SGD",
                "HKD",
                "NOK",
                "SEK",
                "DKK",
            ]

    def validate_symbol(self, symbol: str) -> bool:
        """Validates currency code format"""
        if not symbol or not isinstance(symbol, str):
            return False

        symbol = symbol.strip().upper()

        # Check for 3-character currency code
        if len(symbol) != 3:
            return False

        # Allow only alphabetic characters
        pattern = r"^[A-Z]{3}$"
        return bool(re.match(pattern, symbol))
