import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core_api.models.common import HealthResponse

# Import routers from core_api
from .core_api.routes import (
    crypto_router,
    economics_router,
    forex_router,
    stocks_router,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Orbis Core API...")
    yield
    logger.info("Shutting down Orbis Core API...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Orbis Core API",
        description="RESTful API for financial data using orbis SDK",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers with /api/v1 prefix
    app.include_router(stocks_router, prefix="/api/v1", tags=["stocks"])
    app.include_router(forex_router, prefix="/api/v1", tags=["forex"])
    app.include_router(crypto_router, prefix="/api/v1", tags=["crypto"])
    app.include_router(economics_router, prefix="/api/v1", tags=["economics"])

    # Health check endpoint
    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Health Check",
        description="Check API health status"
    )
    async def health_check() -> HealthResponse:
        return HealthResponse()

    # Root endpoint
    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "message": "Welcome to Orbis Core API",
            "docs": "/docs",
            "health": "/health"
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
