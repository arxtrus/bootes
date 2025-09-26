
from fastapi import APIRouter, Depends, HTTPException, Query

from ..models.common import ErrorResponse
from ..models.stocks import StockInfoResponse, StockPriceResponse
from ..services.stocks import StockService

router = APIRouter()


def get_stock_service() -> StockService:
    """Dependency to get stock service instance"""
    return StockService()


@router.get(
    "/stocks/{symbol}/price",
    response_model=StockPriceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Symbol not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Stock Price Data",
    description="Retrieve stock price data with OHLCV information for a given symbol"
)
async def get_stock_price(
    symbol: str,
    period: str = Query(
        "1mo",
        description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"
    ),
    interval: str = Query(
        "1d",
        description="Interval: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo"
    ),
    stock_service: StockService = Depends(get_stock_service)
) -> StockPriceResponse:
    """Get stock price data with OHLCV information"""

    result = await stock_service.get_price_data(symbol, period, interval)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/stocks/{symbol}/info",
    response_model=StockInfoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Symbol not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Stock Info",
    description="Retrieve real-time stock quote information"
)
async def get_stock_info(
    symbol: str,
    stock_service: StockService = Depends(get_stock_service)
) -> StockInfoResponse:
    """Get real-time stock quote information"""

    result = await stock_service.get_stock_info(symbol)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]
