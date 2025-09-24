import re
from datetime import datetime
from typing import Any, Optional

import pandas as pd
import requests

from ..config import Config
from ..exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    ValidationException,
)
from ..interfaces.base import BaseDataService


class StockService(BaseDataService):
    """Stock data service based on Yahoo Finance API"""

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"

    def get_data(
        self, symbol: str, interval: str = "1d", period: str = "1y", **kwargs
    ) -> pd.DataFrame:
        """
        Retrieves stock price data.

        Args:
            symbol: Stock symbol (e.g., "AAPL", "MSFT")
            interval: Data interval ("1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo")
            period: Query period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")

        Returns:
            DataFrame: OHLCV data
        """
        if not self.validate_symbol(symbol):
            raise ValidationException(f"Invalid stock symbol: {symbol}", field="symbol")

        formatted_symbol = self._format_symbol(symbol)

        params = {
            "interval": interval,
            "period": period,
            "includePrePost": "false",
            "events": "div,splits",
        }

        url = f"{self.base_url}/{formatted_symbol}"

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if "chart" not in data or not data["chart"]["result"]:
                raise DataNotFoundException(
                    f"No data found for symbol: {symbol}", symbol=symbol
                )

            result = data["chart"]["result"][0]

            if "timestamp" not in result or not result["timestamp"]:
                raise DataNotFoundException(
                    f"No timestamp data for symbol: {symbol}", symbol=symbol
                )

            return self._parse_yahoo_data(result, symbol)

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch data for {symbol}: {str(e)}", original_error=e
            ) from e
        except KeyError as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def get_quote(self, symbol: str) -> dict[str, Any]:
        """
        Retrieves real-time stock quote information.

        Args:
            symbol: Stock symbol

        Returns:
            Dict: Real-time stock quote data
        """
        if not self.validate_symbol(symbol):
            raise ValidationException(f"Invalid stock symbol: {symbol}", field="symbol")

        formatted_symbol = self._format_symbol(symbol)
        url = "https://query1.finance.yahoo.com/v6/finance/quote"

        params = {"symbols": formatted_symbol}

        try:
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()

            data = response.json()

            if "quoteResponse" not in data or not data["quoteResponse"]["result"]:
                raise DataNotFoundException(
                    f"No quote data found for symbol: {symbol}", symbol=symbol
                )

            quote = data["quoteResponse"]["result"][0]

            return {
                "symbol": quote.get("symbol"),
                "shortName": quote.get("shortName"),
                "longName": quote.get("longName"),
                "regularMarketPrice": quote.get("regularMarketPrice"),
                "regularMarketChange": quote.get("regularMarketChange"),
                "regularMarketChangePercent": quote.get("regularMarketChangePercent"),
                "regularMarketVolume": quote.get("regularMarketVolume"),
                "marketCap": quote.get("marketCap"),
                "currency": quote.get("currency"),
                "exchangeName": quote.get("fullExchangeName"),
                "marketState": quote.get("marketState"),
                "timestamp": datetime.now().isoformat(),
            }

        except requests.RequestException as e:
            raise NetworkException(
                f"Failed to fetch quote for {symbol}: {str(e)}", original_error=e
            ) from e
        except (KeyError, IndexError) as e:
            raise APIException(f"Unexpected API response format: {str(e)}") from e

    def validate_symbol(self, symbol: str) -> bool:
        """Validates stock symbol format"""
        if not symbol or not isinstance(symbol, str):
            return False

        symbol = symbol.strip()
        if len(symbol) == 0 or len(symbol) > 10:
            return False

        # Basic symbol pattern check (allows alphanumeric, dots, hyphens)
        pattern = r"^[A-Za-z0-9.-]+$"
        return bool(re.match(pattern, symbol))

    def _parse_yahoo_data(self, result: dict[str, Any], symbol: str) -> pd.DataFrame:
        """Converts Yahoo Finance API response to DataFrame"""
        timestamps = result["timestamp"]
        indicators = result["indicators"]["quote"][0]

        # Extract basic OHLCV data
        data = {
            "timestamp": [datetime.fromtimestamp(ts) for ts in timestamps],
            "open": indicators.get("open", [None] * len(timestamps)),
            "high": indicators.get("high", [None] * len(timestamps)),
            "low": indicators.get("low", [None] * len(timestamps)),
            "close": indicators.get("close", [None] * len(timestamps)),
            "volume": indicators.get("volume", [None] * len(timestamps)),
        }

        # Add adjusted close price if available
        if "adjclose" in result["indicators"]:
            adj_close = result["indicators"]["adjclose"][0]["adjclose"]
            data["adj_close"] = adj_close

        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        df["symbol"] = symbol

        # Remove NaN values
        df = df.dropna()

        return df
