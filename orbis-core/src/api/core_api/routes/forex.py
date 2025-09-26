from fastapi import APIRouter, Depends, HTTPException, Query

from ..models.common import ErrorResponse
from ..models.forex import (
    ForexRateResponse,
    MajorPairsResponse,
    SupportedCurrenciesResponse,
)
from ..services.forex import ForexService

router = APIRouter()


def get_forex_service() -> ForexService:
    """Dependency to get forex service instance"""
    return ForexService()


@router.get(
    "/forex/{pair}/rate",
    response_model=ForexRateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Currency pair not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Forex Rate",
    description="Get forex exchange rate for currency pair (e.g., USD-EUR, USD-KRW)"
)
async def get_forex_rate(
    pair: str,
    period: str = Query("1mo", description="Period for historical data"),
    forex_service: ForexService = Depends(get_forex_service)
) -> ForexRateResponse:
    """Get forex exchange rate for currency pair"""

    result = await forex_service.get_forex_rate(pair, period)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/forex/major-pairs",
    response_model=MajorPairsResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Major Pairs",
    description="Get exchange rates for major currency pairs"
)
async def get_major_pairs(
    forex_service: ForexService = Depends(get_forex_service)
) -> MajorPairsResponse:
    """Get exchange rates for major currency pairs"""

    result = await forex_service.get_major_pairs()

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/forex/supported-currencies",
    response_model=SupportedCurrenciesResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Supported Currencies",
    description="Get list of supported currencies"
)
async def get_supported_currencies(
    forex_service: ForexService = Depends(get_forex_service)
) -> SupportedCurrenciesResponse:
    """Get list of supported currencies"""

    result = await forex_service.get_supported_currencies()

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]
