import logging

# Import orbis SDK
import sys
from abc import ABC
from typing import Any, Dict

sys.path.append('../../../../orbis-sdk/src')
from orbis.sdk.exceptions import (
    DataNotFoundException,
    OrbisSDKException,
    ValidationException,
)


class BaseService(ABC):
    """Base service class with common functionality"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle_sdk_exception(self, e: Exception, context: str = "") -> Dict[str, Any]:
        """Handle SDK exceptions and return appropriate error response"""
        if isinstance(e, ValidationException):
            self.logger.warning(f"Validation error {context}: {str(e)}")
            return {"status_code": 400, "error": str(e)}

        elif isinstance(e, DataNotFoundException):
            self.logger.warning(f"Data not found {context}: {str(e)}")
            return {"status_code": 404, "error": str(e)}

        elif isinstance(e, OrbisSDKException):
            self.logger.error(f"SDK error {context}: {str(e)}")
            return {"status_code": 500, "error": "Failed to fetch data"}

        else:
            self.logger.error(f"Unexpected error {context}: {str(e)}")
            return {"status_code": 500, "error": "Internal server error"}
