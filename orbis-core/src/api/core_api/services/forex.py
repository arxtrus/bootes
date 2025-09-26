# Import orbis SDK
import sys
from typing import Any, Dict

sys.path.append('../../../../orbis-sdk/src')
from orbis.sdk.exceptions import ValidationException
from orbis.sdk.services.forex import ForexService as SDKForexService

from ..models.forex import (
    ForexRateResponse,
    MajorPairsResponse,
    SupportedCurrenciesResponse,
)
from .base import BaseService


class ForexService(BaseService):
    """Forex service layer"""

    def __init__(self):
        super().__init__()
        self.sdk_service = SDKForexService()

    def parse_currency_pair(self, pair: str) -> tuple[str, str]:
        """Parse currency pair string into from and to currencies"""
        if '-' in pair:
            from_currency, to_currency = pair.split('-')
        elif '/' in pair:
            from_currency, to_currency = pair.split('/')
        else:
            raise ValidationException("Invalid currency pair format. Use USD-EUR or USD/EUR")

        return from_currency.strip().upper(), to_currency.strip().upper()

    async def get_forex_rate(self, pair: str, period: str = "1mo") -> Dict[str, Any]:
        """Get forex exchange rate for currency pair"""
        try:
            from_currency, to_currency = self.parse_currency_pair(pair)

            self.logger.info(f"Fetching forex rate for {from_currency} to {to_currency}")

            # Get exchange rate from SDK
            rate_data = self.sdk_service.get_rate(from_currency, to_currency)

            # Return structured response
            return {
                "success": True,
                "data": ForexRateResponse(
                    pair=f"{from_currency}/{to_currency}",
                    rate_data=rate_data,
                    period=period
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for pair {pair}")
            return {"success": False, **error_info}

    async def get_major_pairs(self) -> Dict[str, Any]:
        """Get exchange rates for major currency pairs"""
        try:
            self.logger.info("Fetching major currency pairs")

            # Get major pairs data from SDK
            major_data = self.sdk_service.get_major_pairs()

            # Return structured response
            return {
                "success": True,
                "data": MajorPairsResponse(major_pairs=major_data)
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, "for major pairs")
            return {"success": False, **error_info}

    async def get_supported_currencies(self) -> Dict[str, Any]:
        """Get list of supported currencies"""
        try:
            self.logger.info("Fetching supported currencies")

            # Get supported currencies from SDK
            currencies = self.sdk_service.get_supported_currencies()

            # Return structured response
            return {
                "success": True,
                "data": SupportedCurrenciesResponse(supported_currencies=currencies)
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, "for supported currencies")
            return {"success": False, **error_info}
