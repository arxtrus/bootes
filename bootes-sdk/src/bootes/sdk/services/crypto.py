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


class CryptoService(BaseDataService):
    """Cryptocurrency data service based on CoinGecko API"""

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_data(
        self, symbol: str, vs_currency: str = "usd", **kwargs
    ) -> dict[str, Any]:
        """
        Retrieves cryptocurrency price data.

        Args:
            symbol: Cryptocurrency symbol (e.g., "bitcoin", "ethereum")
            vs_currency: Base currency (e.g., "usd", "krw")

        Returns:
            Dict: Cryptocurrency price data
        """
        if not self.validate_symbol(symbol):
            raise ValidationException(
                f"Invalid crypto symbol: {symbol}", field="symbol"
            )

        formatted_symbol = symbol.lower().strip()
        url = f"{self.base_url}/simple/price"

        params = {
            "ids": formatted_symbol,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true",
        }

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if not data or formatted_symbol not in data:
                raise DataNotFoundException(
                    f"No data found for symbol: {symbol}", symbol=symbol
                )

            crypto_data = data[formatted_symbol]

            return {
                "symbol": formatted_symbol,
                "price": crypto_data.get(vs_currency),
                "market_cap": crypto_data.get(f"{vs_currency}_market_cap"),
                "volume_24h": crypto_data.get(f"{vs_currency}_24h_vol"),
                "change_24h": crypto_data.get(f"{vs_currency}_24h_change"),
                "vs_currency": vs_currency,
                "last_updated": (
                    datetime.fromtimestamp(
                        crypto_data.get("last_updated_at", 0)
                    ).isoformat()
                    if crypto_data.get("last_updated_at")
                    else None
                ),
                "timestamp": datetime.now().isoformat(),
            }

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch data for {symbol}: {str(e)}", original_error=e
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def get_market_data(self, symbol: str, vs_currency: str = "usd") -> dict[str, Any]:
        """
        Retrieves detailed market data.

        Args:
            symbol: Cryptocurrency symbol
            vs_currency: Base currency

        Returns:
            Dict: Detailed market data
        """
        if not self.validate_symbol(symbol):
            raise ValidationException(
                f"Invalid crypto symbol: {symbol}", field="symbol"
            )

        formatted_symbol = symbol.lower().strip()
        url = f"{self.base_url}/coins/{formatted_symbol}"

        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false",
        }

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if "market_data" not in data:
                raise DataNotFoundException(
                    f"No market data found for symbol: {symbol}", symbol=symbol
                )

            market_data = data["market_data"]
            current_price = market_data.get("current_price", {})

            return {
                "id": data.get("id"),
                "symbol": data.get("symbol"),
                "name": data.get("name"),
                "current_price": current_price.get(vs_currency),
                "market_cap": market_data.get("market_cap", {}).get(vs_currency),
                "market_cap_rank": market_data.get("market_cap_rank"),
                "total_volume": market_data.get("total_volume", {}).get(vs_currency),
                "high_24h": market_data.get("high_24h", {}).get(vs_currency),
                "low_24h": market_data.get("low_24h", {}).get(vs_currency),
                "price_change_24h": market_data.get("price_change_24h"),
                "price_change_percentage_24h": market_data.get(
                    "price_change_percentage_24h"
                ),
                "circulating_supply": market_data.get("circulating_supply"),
                "total_supply": market_data.get("total_supply"),
                "max_supply": market_data.get("max_supply"),
                "ath": market_data.get("ath", {}).get(vs_currency),
                "atl": market_data.get("atl", {}).get(vs_currency),
                "vs_currency": vs_currency,
                "last_updated": data.get("last_updated"),
                "timestamp": datetime.now().isoformat(),
            }

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch market data for {symbol}: {str(e)}", original_error=e
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def get_top_cryptos(
        self, vs_currency: str = "usd", limit: int = 10
    ) -> list[dict[str, Any]]:
        """
        Retrieves top cryptocurrencies by market cap.

        Args:
            vs_currency: Base currency
            limit: Number of results to retrieve (max 250)

        Returns:
            List[Dict]: List of top cryptocurrencies
        """
        if limit > 250:
            limit = 250
        elif limit < 1:
            limit = 10

        url = f"{self.base_url}/coins/markets"

        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": "false",
        }

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise DataNotFoundException("No top crypto data available")

            result = []
            for crypto in data:
                result.append(
                    {
                        "id": crypto.get("id"),
                        "symbol": crypto.get("symbol"),
                        "name": crypto.get("name"),
                        "current_price": crypto.get("current_price"),
                        "market_cap": crypto.get("market_cap"),
                        "market_cap_rank": crypto.get("market_cap_rank"),
                        "total_volume": crypto.get("total_volume"),
                        "price_change_percentage_24h": crypto.get(
                            "price_change_percentage_24h"
                        ),
                        "vs_currency": vs_currency,
                    }
                )

            return result

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch top cryptos: {str(e)}", original_error=e
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def search_crypto(self, query: str) -> list[dict[str, Any]]:
        """
        Searches for cryptocurrencies.

        Args:
            query: Search query

        Returns:
            List[Dict]: Search results
        """
        if not query or len(query.strip()) < 2:
            raise ValidationException(
                "Query must be at least 2 characters", field="query"
            )

        url = f"{self.base_url}/search"
        params = {"query": query.strip()}

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if "coins" not in data:
                return []

            result = []
            for coin in data["coins"]:
                result.append(
                    {
                        "id": coin.get("id"),
                        "name": coin.get("name"),
                        "symbol": coin.get("symbol"),
                        "market_cap_rank": coin.get("market_cap_rank"),
                        "thumb": coin.get("thumb"),
                        "large": coin.get("large"),
                    }
                )

            return result

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to search crypto: {str(e)}", original_error=e
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def validate_symbol(self, symbol: str) -> bool:
        """Validates cryptocurrency symbol format"""
        if not symbol or not isinstance(symbol, str):
            return False

        symbol = symbol.strip()
        if len(symbol) == 0 or len(symbol) > 50:
            return False

        # Basic symbol pattern check (allows alphanumeric, hyphens)
        pattern = r"^[a-zA-Z0-9-]+$"
        return bool(re.match(pattern, symbol))
