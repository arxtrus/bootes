"""
Tests for Exception classes
"""

from orbis.sdk.exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    OrbisSDKException,
    RateLimitException,
    ValidationException,
)


class TestOrbisSDKException:
    def test_basic_exception(self):
        """Test basic OrbisSDKException"""
        exc = OrbisSDKException("Test message")

        assert str(exc) == "Test message"
        assert exc.message == "Test message"
        assert exc.error_code is None
        assert exc.details is None

    def test_exception_with_error_code(self):
        """Test OrbisSDKException with error code"""
        exc = OrbisSDKException("Test message", error_code="TEST_ERROR")

        assert str(exc) == "[TEST_ERROR] Test message"
        assert exc.message == "Test message"
        assert exc.error_code == "TEST_ERROR"
        assert exc.details is None

    def test_exception_with_details(self):
        """Test OrbisSDKException with details"""
        details = {"key": "value", "number": 42}
        exc = OrbisSDKException("Test message", details=details)

        assert exc.details == details
        assert exc.details["key"] == "value"
        assert exc.details["number"] == 42

    def test_exception_with_all_parameters(self):
        """Test OrbisSDKException with all parameters"""
        details = {"debug_info": "Some debug data"}
        exc = OrbisSDKException(
            "Test message", error_code="FULL_ERROR", details=details
        )

        assert str(exc) == "[FULL_ERROR] Test message"
        assert exc.message == "Test message"
        assert exc.error_code == "FULL_ERROR"
        assert exc.details == details

    def test_exception_inheritance(self):
        """Test that OrbisSDKException inherits from Exception"""
        exc = OrbisSDKException("Test message")

        assert isinstance(exc, Exception)
        assert isinstance(exc, OrbisSDKException)


class TestAPIException:
    def test_api_exception_basic(self):
        """Test basic APIException"""
        exc = APIException("API error occurred")

        assert str(exc) == "[API_ERROR] API error occurred"
        assert exc.message == "API error occurred"
        assert exc.error_code == "API_ERROR"
        assert exc.status_code is None
        assert exc.response_data is None

    def test_api_exception_with_status_code(self):
        """Test APIException with status code"""
        exc = APIException("Server error", status_code=500)

        assert exc.status_code == 500
        assert exc.error_code == "API_ERROR"

    def test_api_exception_with_response_data(self):
        """Test APIException with response data"""
        response_data = {"error": "Invalid request", "code": 400}
        exc = APIException("Bad request", response_data=response_data)

        assert exc.response_data == response_data
        assert exc.response_data["error"] == "Invalid request"

    def test_api_exception_inheritance(self):
        """Test APIException inheritance"""
        exc = APIException("API error")

        assert isinstance(exc, OrbisSDKException)
        assert isinstance(exc, APIException)


class TestDataNotFoundException:
    def test_data_not_found_basic(self):
        """Test basic DataNotFoundException"""
        exc = DataNotFoundException()

        assert str(exc) == "[DATA_NOT_FOUND] Requested data not found"
        assert exc.message == "Requested data not found"
        assert exc.error_code == "DATA_NOT_FOUND"
        assert exc.symbol is None

    def test_data_not_found_custom_message(self):
        """Test DataNotFoundException with custom message"""
        exc = DataNotFoundException("Custom not found message")

        assert exc.message == "Custom not found message"
        assert str(exc) == "[DATA_NOT_FOUND] Custom not found message"

    def test_data_not_found_with_symbol(self):
        """Test DataNotFoundException with symbol"""
        exc = DataNotFoundException("Symbol not found", symbol="AAPL")

        assert exc.symbol == "AAPL"
        assert exc.message == "Symbol not found"

    def test_data_not_found_inheritance(self):
        """Test DataNotFoundException inheritance"""
        exc = DataNotFoundException()

        assert isinstance(exc, OrbisSDKException)
        assert isinstance(exc, DataNotFoundException)


class TestRateLimitException:
    def test_rate_limit_basic(self):
        """Test basic RateLimitException"""
        exc = RateLimitException()

        assert str(exc) == "[RATE_LIMIT] API rate limit exceeded"
        assert exc.message == "API rate limit exceeded"
        assert exc.error_code == "RATE_LIMIT"
        assert exc.retry_after is None

    def test_rate_limit_custom_message(self):
        """Test RateLimitException with custom message"""
        exc = RateLimitException("Custom rate limit message")

        assert exc.message == "Custom rate limit message"
        assert str(exc) == "[RATE_LIMIT] Custom rate limit message"

    def test_rate_limit_with_retry_after(self):
        """Test RateLimitException with retry_after"""
        exc = RateLimitException("Rate limited", retry_after=60)

        assert exc.retry_after == 60
        assert exc.message == "Rate limited"

    def test_rate_limit_inheritance(self):
        """Test RateLimitException inheritance"""
        exc = RateLimitException()

        assert isinstance(exc, OrbisSDKException)
        assert isinstance(exc, RateLimitException)


class TestValidationException:
    def test_validation_exception_basic(self):
        """Test basic ValidationException"""
        exc = ValidationException("Invalid input")

        assert str(exc) == "[VALIDATION_ERROR] Invalid input"
        assert exc.message == "Invalid input"
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.field is None

    def test_validation_exception_with_field(self):
        """Test ValidationException with field"""
        exc = ValidationException("Invalid symbol format", field="symbol")

        assert exc.field == "symbol"
        assert exc.message == "Invalid symbol format"

    def test_validation_exception_inheritance(self):
        """Test ValidationException inheritance"""
        exc = ValidationException("Invalid input")

        assert isinstance(exc, OrbisSDKException)
        assert isinstance(exc, ValidationException)


class TestNetworkException:
    def test_network_exception_basic(self):
        """Test basic NetworkException"""
        exc = NetworkException("Network connection failed")

        assert str(exc) == "[NETWORK_ERROR] Network connection failed"
        assert exc.message == "Network connection failed"
        assert exc.error_code == "NETWORK_ERROR"
        assert exc.original_error is None

    def test_network_exception_with_original_error(self):
        """Test NetworkException with original error"""
        original = Exception("Connection timeout")
        exc = NetworkException("Network failed", original_error=original)

        assert exc.original_error is original
        assert exc.original_error.args[0] == "Connection timeout"

    def test_network_exception_inheritance(self):
        """Test NetworkException inheritance"""
        exc = NetworkException("Network error")

        assert isinstance(exc, OrbisSDKException)
        assert isinstance(exc, NetworkException)


class TestExceptionHierarchy:
    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from OrbisSDKException"""
        exceptions = [
            APIException("API error"),
            DataNotFoundException("Not found"),
            RateLimitException("Rate limited"),
            ValidationException("Invalid"),
            NetworkException("Network error"),
        ]

        for exc in exceptions:
            assert isinstance(exc, OrbisSDKException)
            assert isinstance(exc, Exception)

    def test_exception_error_codes(self):
        """Test that exceptions have correct error codes"""
        test_cases = [
            (APIException("test"), "API_ERROR"),
            (DataNotFoundException("test"), "DATA_NOT_FOUND"),
            (RateLimitException("test"), "RATE_LIMIT"),
            (ValidationException("test"), "VALIDATION_ERROR"),
            (NetworkException("test"), "NETWORK_ERROR"),
        ]

        for exc, expected_code in test_cases:
            assert exc.error_code == expected_code

    def test_exception_str_format(self):
        """Test string formatting of exceptions"""
        exc = OrbisSDKException("Test message", error_code="TEST_CODE")
        assert str(exc) == "[TEST_CODE] Test message"

        exc_no_code = OrbisSDKException("Test message")
        assert str(exc_no_code) == "Test message"

    def test_exception_with_none_values(self):
        """Test exceptions handle None values properly"""
        exc = OrbisSDKException("Test", error_code=None, details=None)
        assert exc.error_code is None
        assert exc.details is None
        assert str(exc) == "Test"

    def test_exception_pickleable(self):
        """Test that exceptions can be pickled (for multiprocessing)"""
        import pickle

        exc = OrbisSDKException(
            "Test message", error_code="TEST", details={"key": "value"}
        )
        pickled = pickle.dumps(exc)
        unpickled = pickle.loads(pickled)

        assert unpickled.message == exc.message
        assert unpickled.error_code == exc.error_code
        assert unpickled.details == exc.details
        assert str(unpickled) == str(exc)
