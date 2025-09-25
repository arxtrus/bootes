"""
orbis SDK - Financial Data Collection Library

A Python SDK for collecting financial data from various sources including stocks,
forex, and cryptocurrency markets. Designed for integration with FastAPI backends.
"""

from .config import Config, get_config
from .exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    OrbisSDKException,
    RateLimitException,
    ValidationException,
)
from .services import CryptoService, ForexService, StockService

__version__ = "0.1.0"
__author__ = "arxtrus orbis team"
__email__ = "orbis@arxtrus.com"

__all__ = [
    # Core services
    "StockService",
    "ForexService",
    "CryptoService",
    # Configuration
    "Config",
    "get_config",
    # Exceptions
    "OrbisSDKException",
    "APIException",
    "DataNotFoundException",
    "RateLimitException",
    "ValidationException",
    "NetworkException",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
]


class OrbisSDK:
    """메인 SDK 클래스 - 모든 서비스에 대한 통합 접근점"""

    def __init__(self, config: Config = None):
        self.config = config or get_config()

        # 서비스 인스턴스 초기화
        self._stock = None
        self._forex = None
        self._crypto = None

    @property
    def stock(self) -> StockService:
        """주식 데이터 서비스"""
        if self._stock is None:
            self._stock = StockService(self.config)
        return self._stock

    @property
    def forex(self) -> ForexService:
        """외환 데이터 서비스"""
        if self._forex is None:
            self._forex = ForexService(self.config)
        return self._forex

    @property
    def crypto(self) -> CryptoService:
        """암호화폐 데이터 서비스"""
        if self._crypto is None:
            self._crypto = CryptoService(self.config)
        return self._crypto
