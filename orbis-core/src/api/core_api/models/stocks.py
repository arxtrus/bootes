from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .common import BaseResponse


class StockPriceData(BaseModel):
    """Individual stock price data point"""
    timestamp: datetime
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    adj_close: Optional[float] = Field(None, alias="adj_close")
    symbol: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StockPriceRequest(BaseModel):
    """Stock price request parameters"""
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL, MSFT)")
    period: str = Field("1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    interval: str = Field("1d", description="Interval: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo")


class StockPriceResponse(BaseResponse):
    """Stock price response with OHLCV data"""
    symbol: str
    period: str
    interval: str
    data: list[StockPriceData]
    count: int

    def __init__(self, symbol: str, period: str, interval: str, data: list[StockPriceData], **kwargs):
        super().__init__(
            symbol=symbol.upper(),
            period=period,
            interval=interval,
            data=data,
            count=len(data),
            **kwargs
        )


class StockQuoteInfo(BaseModel):
    """Stock quote information"""
    symbol: Optional[str] = None
    short_name: Optional[str] = Field(None, alias="shortName")
    long_name: Optional[str] = Field(None, alias="longName")
    regular_market_price: Optional[float] = Field(None, alias="regularMarketPrice")
    regular_market_change: Optional[float] = Field(None, alias="regularMarketChange")
    regular_market_change_percent: Optional[float] = Field(None, alias="regularMarketChangePercent")
    regular_market_volume: Optional[int] = Field(None, alias="regularMarketVolume")
    market_cap: Optional[int] = Field(None, alias="marketCap")
    currency: Optional[str] = None
    exchange_name: Optional[str] = Field(None, alias="exchangeName")
    market_state: Optional[str] = Field(None, alias="marketState")
    timestamp: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class StockInfoResponse(BaseResponse):
    """Stock info response with quote data"""
    symbol: str
    info: StockQuoteInfo

    def __init__(self, symbol: str, info: dict, **kwargs):
        quote_info = StockQuoteInfo(**info) if isinstance(info, dict) else info
        super().__init__(
            symbol=symbol.upper(),
            info=quote_info,
            **kwargs
        )
