# Import orbis SDK
import sys
from typing import Any

import pandas as pd

sys.path.append('../../../../orbis-sdk/src')
from orbis.sdk.services.stock import StockService as SDKStockService

from ..models.stocks import StockInfoResponse, StockPriceData, StockPriceResponse
from .base import BaseService


class StockService(BaseService):
    """Stock service layer"""

    def __init__(self):
        super().__init__()
        self.sdk_service = SDKStockService()

    def dataframe_to_stock_data(self, df: pd.DataFrame) -> list[StockPriceData]:
        """Convert pandas DataFrame to StockPriceData list"""
        if df.empty:
            return []

        stock_data = []
        df_reset = df.reset_index()

        for _, row in df_reset.iterrows():
            # Handle datetime conversion
            timestamp = row['timestamp']
            if hasattr(timestamp, 'isoformat'):
                timestamp_iso = timestamp
            else:
                timestamp_iso = pd.to_datetime(timestamp)

            stock_data.append(StockPriceData(
                timestamp=timestamp_iso,
                open=None if pd.isna(row.get('open')) else float(row.get('open')),
                high=None if pd.isna(row.get('high')) else float(row.get('high')),
                low=None if pd.isna(row.get('low')) else float(row.get('low')),
                close=None if pd.isna(row.get('close')) else float(row.get('close')),
                volume=None if pd.isna(row.get('volume')) else int(row.get('volume')),
                adj_close=None if pd.isna(row.get('adj_close')) else float(row.get('adj_close')),
                symbol=row.get('symbol', '')
            ))

        return stock_data

    async def get_price_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> dict[str, Any]:
        """Get stock price data"""
        try:
            self.logger.info(f"Fetching stock price data for {symbol}")

            # Get data from SDK
            df = self.sdk_service.get_data(symbol=symbol, period=period, interval=interval)

            # Convert to structured data
            stock_data = self.dataframe_to_stock_data(df)

            # Return structured response
            return {
                "success": True,
                "data": StockPriceResponse(
                    symbol=symbol,
                    period=period,
                    interval=interval,
                    data=stock_data
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for symbol {symbol}")
            return {"success": False, **error_info}

    async def get_stock_info(self, symbol: str) -> dict[str, Any]:
        """Get stock quote information"""
        try:
            self.logger.info(f"Fetching stock info for {symbol}")

            # Get quote data from SDK
            quote_data = self.sdk_service.get_quote(symbol=symbol)

            # Return structured response
            return {
                "success": True,
                "data": StockInfoResponse(
                    symbol=symbol,
                    info=quote_data
                )
            }

        except Exception as e:
            error_info = self.handle_sdk_exception(e, f"for symbol {symbol}")
            return {"success": False, **error_info}
