from fastapi import APIRouter, HTTPException, Depends

from ..services.economics import EconomicsService
from ..models.economics import EconomicIndicatorResponse, IndicatorListResponse
from ..models.common import ErrorResponse

router = APIRouter()


def get_economics_service() -> EconomicsService:
    """Dependency to get economics service instance"""
    return EconomicsService()


@router.get(
    "/economics/{indicator}",
    response_model=EconomicIndicatorResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Economic indicator not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Economic Indicator",
    description="Get economic indicator data (placeholder implementation)"
)
async def get_economic_indicator(
    indicator: str,
    economics_service: EconomicsService = Depends(get_economics_service)
) -> EconomicIndicatorResponse:
    """Get economic indicator data"""
    
    result = await economics_service.get_economic_indicator(indicator)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )
    
    return result["data"]


@router.get(
    "/economics/indicators",
    response_model=IndicatorListResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="List Economic Indicators",
    description="List available economic indicators"
)
async def list_economic_indicators(
    economics_service: EconomicsService = Depends(get_economics_service)
) -> IndicatorListResponse:
    """List available economic indicators"""
    
    result = await economics_service.list_economic_indicators()
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail={"error": result["error"]}
        )
    
    return result["data"]