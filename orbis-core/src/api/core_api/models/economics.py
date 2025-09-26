from typing import Dict

from pydantic import BaseModel

from .common import BaseResponse


class EconomicIndicatorData(BaseModel):
    """Economic indicator data"""
    message: str
    status: str


class EconomicIndicatorResponse(BaseResponse):
    """Economic indicator response"""
    indicator: str
    name: str
    data: EconomicIndicatorData
    note: str

    def __init__(self, indicator: str, name: str, data: dict, note: str, **kwargs):
        indicator_data = EconomicIndicatorData(**data) if isinstance(data, dict) else data
        super().__init__(
            indicator=indicator.lower(),
            name=name,
            data=indicator_data,
            note=note,
            **kwargs
        )


class IndicatorInfo(BaseModel):
    """Individual indicator information"""
    name: str
    description: str
    status: str


class IndicatorListResponse(BaseResponse):
    """Economic indicators list response"""
    indicators: Dict[str, IndicatorInfo]
    count: int
    note: str

    def __init__(self, indicators: Dict[str, dict], note: str, **kwargs):
        indicator_items = {
            key: IndicatorInfo(**value) if isinstance(value, dict) else value
            for key, value in indicators.items()
        }
        super().__init__(
            indicators=indicator_items,
            count=len(indicator_items),
            note=note,
            **kwargs
        )
