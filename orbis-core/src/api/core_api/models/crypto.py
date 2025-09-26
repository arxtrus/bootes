from typing import List, Optional

from pydantic import BaseModel, Field

from .common import BaseResponse


class CryptoPriceData(BaseModel):
    """Cryptocurrency price data"""
    symbol: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = Field(None, alias="volume_24h")
    change_24h: Optional[float] = Field(None, alias="change_24h")
    vs_currency: str
    last_updated: Optional[str] = None
    timestamp: str

    class Config:
        allow_population_by_field_name = True


class CryptoPriceResponse(BaseResponse):
    """Crypto price response"""
    symbol: str
    currency: str
    price_data: CryptoPriceData

    def __init__(self, symbol: str, currency: str, price_data: dict, **kwargs):
        price_info = CryptoPriceData(**price_data) if isinstance(price_data, dict) else price_data
        super().__init__(
            symbol=symbol.upper(),
            currency=currency.upper(),
            price_data=price_info,
            **kwargs
        )


class CryptoMarketData(BaseModel):
    """Detailed crypto market data"""
    id: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    market_cap_rank: Optional[int] = None
    total_volume: Optional[float] = None
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    ath: Optional[float] = None  # All-time high
    atl: Optional[float] = None  # All-time low
    vs_currency: str
    last_updated: Optional[str] = None
    timestamp: str


class CryptoMarketResponse(BaseResponse):
    """Crypto market data response"""
    symbol: str
    currency: str
    market_data: CryptoMarketData

    def __init__(self, symbol: str, currency: str, market_data: dict, **kwargs):
        market_info = CryptoMarketData(**market_data) if isinstance(market_data, dict) else market_data
        super().__init__(
            symbol=symbol.upper(),
            currency=currency.upper(),
            market_data=market_info,
            **kwargs
        )


class TopCryptoItem(BaseModel):
    """Individual top crypto item"""
    id: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    market_cap_rank: Optional[int] = None
    total_volume: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    vs_currency: str


class TopCryptosResponse(BaseResponse):
    """Top cryptocurrencies response"""
    currency: str
    limit: int
    top_cryptos: List[TopCryptoItem]
    count: int

    def __init__(self, currency: str, limit: int, top_cryptos: List[dict], **kwargs):
        crypto_items = [TopCryptoItem(**crypto) for crypto in top_cryptos]
        super().__init__(
            currency=currency.upper(),
            limit=limit,
            top_cryptos=crypto_items,
            count=len(crypto_items),
            **kwargs
        )


class CryptoSearchItem(BaseModel):
    """Crypto search result item"""
    id: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    market_cap_rank: Optional[int] = None
    thumb: Optional[str] = None
    large: Optional[str] = None


class CryptoSearchResponse(BaseResponse):
    """Crypto search response"""
    query: str
    results: List[CryptoSearchItem]
    count: int

    def __init__(self, query: str, results: List[dict], **kwargs):
        search_items = [CryptoSearchItem(**item) for item in results]
        super().__init__(
            query=query,
            results=search_items,
            count=len(search_items),
            **kwargs
        )
