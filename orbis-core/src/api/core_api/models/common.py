from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    timestamp: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = "healthy"
    service: str = "orbis-core-api"
    version: str = "0.1.0"
    timestamp: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DataListResponse(BaseResponse):
    """Generic response for list data"""
    data: list
    count: int
    
    def __init__(self, data: list, **kwargs):
        super().__init__(data=data, count=len(data), **kwargs)