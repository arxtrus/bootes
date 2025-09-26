# Import orbis SDK
import sys
from typing import Any, Dict

sys.path.append('../../../../orbis-sdk/src')
from orbis.sdk.services.crypto import CryptoService as SDKCryptoService

from ..models.crypto import (
    CryptoMarketResponse,
    CryptoPriceResponse,
    CryptoSearchResponse,
    TopCryptosResponse,
)
from .base import BaseService


class CryptoService(BaseService):
    """Crypto service layer"""

    def __init__(self):
        super().__init__()
        self.sdk_service = SDKCryptoService()

    async def get_crypto_price(self, symbol: str, currency: str = "USD") -> Dict[str, Any]:
        """Get cryptocurrency price data"""
        try:
            self.logger.info(f"Fetching crypto price for {symbol} in {currency}")

            # Get price data from SDK
            price_data = self.sdk_service.get_data(
                symbol=symbol.lower(),
                vs_currency=currency.lower()
            )

            # Return structured response
            return {
                "success": True,
                "data": CryptoPriceResponse(
                    symbol=symbol,
                    currency=currency,
                    price_data=price_data
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for {symbol}")
            return {"success": False, **error_info}

    async def get_crypto_market_data(self, symbol: str, currency: str = "USD") -> Dict[str, Any]:
        """Get detailed cryptocurrency market data"""
        try:
            self.logger.info(f"Fetching crypto market data for {symbol} in {currency}")

            # Get market data from SDK
            market_data = self.sdk_service.get_market_data(
                symbol=symbol.lower(),
                vs_currency=currency.lower()
            )

            # Return structured response
            return {
                "success": True,
                "data": CryptoMarketResponse(
                    symbol=symbol,
                    currency=currency,
                    market_data=market_data
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for {symbol} market data")
            return {"success": False, **error_info}

    async def get_top_cryptos(self, currency: str = "USD", limit: int = 10) -> Dict[str, Any]:
        """Get top cryptocurrencies by market cap"""
        try:
            self.logger.info(f"Fetching top {limit} cryptocurrencies in {currency}")

            # Get top cryptos from SDK
            top_cryptos = self.sdk_service.get_top_cryptos(
                vs_currency=currency.lower(),
                limit=limit
            )

            # Return structured response
            return {
                "success": True,
                "data": TopCryptosResponse(
                    currency=currency,
                    limit=limit,
                    top_cryptos=top_cryptos
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, "for top cryptos")
            return {"success": False, **error_info}

    async def search_crypto(self, query: str) -> Dict[str, Any]:
        """Search for cryptocurrencies"""
        try:
            self.logger.info(f"Searching cryptocurrencies with query: {query}")

            # Search cryptos from SDK
            search_results = self.sdk_service.search_crypto(query)

            # Return structured response
            return {
                "success": True,
                "data": CryptoSearchResponse(
                    query=query,
                    results=search_results
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for search query {query}")
            return {"success": False, **error_info}
