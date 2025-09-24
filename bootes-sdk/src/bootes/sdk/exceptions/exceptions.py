from typing import Any, Optional


class BootesSDKException(Exception):
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class APIException(BootesSDKException):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
    ):
        super().__init__(message, error_code="API_ERROR")
        self.status_code = status_code
        self.response_data = response_data


class DataNotFoundException(BootesSDKException):
    def __init__(
        self, message: str = "Requested data not found", symbol: Optional[str] = None
    ):
        super().__init__(message, error_code="DATA_NOT_FOUND")
        self.symbol = symbol


class RateLimitException(BootesSDKException):
    def __init__(
        self,
        message: str = "API rate limit exceeded",
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, error_code="RATE_LIMIT")
        self.retry_after = retry_after


class ValidationException(BootesSDKException):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, error_code="VALIDATION_ERROR")
        self.field = field


class NetworkException(BootesSDKException):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message, error_code="NETWORK_ERROR")
        self.original_error = original_error
