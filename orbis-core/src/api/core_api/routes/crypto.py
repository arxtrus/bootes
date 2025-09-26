from fastapi import APIRouter, Depends, HTTPException, Query

from ..models.common import ErrorResponse
from ..models.crypto import (
    CryptoMarketResponse,
    CryptoPriceResponse,
    CryptoSearchResponse,
    TopCryptosResponse,
)
from ..services.crypto import CryptoService

router = APIRouter()


def get_crypto_service() -> CryptoService:
    """Dependency to get crypto service instance"""
    return CryptoService()


@router.get(
    "/crypto/{symbol}/price",
    response_model=CryptoPriceResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Cryptocurrency not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Crypto Price",
    description="Get cryptocurrency price data"
)
async def get_crypto_price(
    symbol: str,
    currency: str = Query("USD", description="Base currency (e.g., USD, KRW, EUR)"),
    crypto_service: CryptoService = Depends(get_crypto_service)
) -> CryptoPriceResponse:
    """Get cryptocurrency price data"""

    result = await crypto_service.get_crypto_price(symbol, currency)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/crypto/{symbol}/market",
    response_model=CryptoMarketResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Cryptocurrency not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Crypto Market Data",
    description="Get detailed cryptocurrency market data"
)
async def get_crypto_market_data(
    symbol: str,
    currency: str = Query("USD", description="Base currency"),
    crypto_service: CryptoService = Depends(get_crypto_service)
) -> CryptoMarketResponse:
    """Get detailed cryptocurrency market data"""

    result = await crypto_service.get_crypto_market_data(symbol, currency)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/crypto/top",
    response_model=TopCryptosResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Top Cryptos",
    description="Get top cryptocurrencies by market cap"
)
async def get_top_cryptos(
    currency: str = Query("USD", description="Base currency"),
    limit: int = Query(10, description="Number of results (max 250)", ge=1, le=250),
    crypto_service: CryptoService = Depends(get_crypto_service)
) -> TopCryptosResponse:
    """Get top cryptocurrencies by market cap"""

    result = await crypto_service.get_top_cryptos(currency, limit)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]


@router.get(
    "/crypto/search",
    response_model=CryptoSearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Search Crypto",
    description="Search for cryptocurrencies"
)
async def search_crypto(
    query: str = Query(..., description="Search query for cryptocurrency", min_length=2),
    crypto_service: CryptoService = Depends(get_crypto_service)
) -> CryptoSearchResponse:
    """Search for cryptocurrencies"""

    result = await crypto_service.search_crypto(query)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )

    return result["data"]
