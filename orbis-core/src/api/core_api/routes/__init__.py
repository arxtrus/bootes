from .stocks import router as stocks_router
from .forex import router as forex_router
from .crypto import router as crypto_router
from .economics import router as economics_router

__all__ = [
    "stocks_router",
    "forex_router",
    "crypto_router", 
    "economics_router",
]