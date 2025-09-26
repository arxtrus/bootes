from typing import Dict, List

from pydantic import BaseModel, Field

from .common import BaseResponse


class ForexRateData(BaseModel):
    """Forex rate data"""
    from_currency: str = Field(..., alias="from")
    to_currency: str = Field(..., alias="to")
    rate: float
    date: str
    timestamp: str

    class Config:
        allow_population_by_field_name = True


class ForexRateResponse(BaseResponse):
    """Forex rate response"""
    pair: str
    rate_data: ForexRateData
    period: str

    def __init__(self, pair: str, rate_data: dict, period: str, **kwargs):
        rate_info = ForexRateData(**rate_data) if isinstance(rate_data, dict) else rate_data
        super().__init__(
            pair=pair,
            rate_data=rate_info,
            period=period,
            **kwargs
        )


class ForexPairResponse(BaseResponse):
    """Single forex pair response"""
    from_currency: str
    to_currency: str
    rate: float
    date: str


class MajorPairsData(BaseModel):
    """Major currency pairs data"""
    base: str
    rates: Dict[str, float]
    date: str
    timestamp: str


class MajorPairsResponse(BaseResponse):
    """Major pairs response"""
    major_pairs: MajorPairsData

    def __init__(self, major_pairs: dict, **kwargs):
        pairs_data = MajorPairsData(**major_pairs) if isinstance(major_pairs, dict) else major_pairs
        super().__init__(
            major_pairs=pairs_data,
            **kwargs
        )


class SupportedCurrenciesResponse(BaseResponse):
    """Supported currencies response"""
    supported_currencies: List[str]
    count: int

    def __init__(self, supported_currencies: List[str], **kwargs):
        super().__init__(
            supported_currencies=supported_currencies,
            count=len(supported_currencies),
            **kwargs
        )
