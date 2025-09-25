"""
Tests for ForexService
"""

from unittest.mock import Mock, patch

import pytest
from orbis.sdk.exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    ValidationException,
)
from orbis.sdk.services.forex import ForexService


class TestForexService:
    def test_init_with_config(self, test_config):
        """Test ForexService initialization with custom config"""
        service = ForexService(test_config)
        assert service.config == test_config
        assert service.base_url == "https://api.exchangerate-api.com/v4/latest"

    def test_init_without_config(self):
        """Test ForexService initialization without config"""
        service = ForexService()
        assert service.config is not None

    def test_validate_symbol_valid(self):
        """Test currency code validation with valid codes"""
        service = ForexService()

        valid_codes = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD"]
        for code in valid_codes:
            assert service.validate_symbol(code) is True

    def test_validate_symbol_invalid(self):
        """Test currency code validation with invalid codes"""
        service = ForexService()

        invalid_codes = ["", "US", "USDD", None, 123, "us$", "USD1"]
        for code in invalid_codes:
            assert service.validate_symbol(code) is False

    @patch("requests.get")
    def test_get_data_success(self, mock_get, test_config, sample_forex_response):
        """Test successful forex data retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_forex_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = ForexService(test_config)
        result = service.get_data("USD")

        assert isinstance(result, dict)
        assert result["base"] == "USD"
        assert result["date"] == "2025-01-01"
        assert "rates" in result
        assert "timestamp" in result
        assert result["rates"]["EUR"] == 0.85
        assert result["rates"]["KRW"] == 1300.0

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "USD" in args[0]
        assert kwargs["timeout"] == test_config.timeout

    @patch("requests.get")
    def test_get_data_invalid_currency(self, mock_get, test_config):
        """Test data retrieval with invalid currency code"""
        service = ForexService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.get_data("INVALID")

        assert "Invalid currency code: INVALID" in str(exc_info.value)
        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_data_no_rates(self, mock_get, test_config):
        """Test data retrieval when no rates are found"""
        mock_response = Mock()
        mock_response.json.return_value = {"base": "USD"}  # Missing rates
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = ForexService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_data("USD")

        assert "No exchange rate data found for: USD" in str(exc_info.value)

    @patch("requests.get")
    def test_get_data_network_error(self, mock_get, test_config):
        """Test data retrieval with network error"""
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        service = ForexService(test_config)

        with pytest.raises(NetworkException) as exc_info:
            service.get_data("USD")

        assert "Failed to fetch forex data for USD" in str(exc_info.value)

    @patch.object(ForexService, "get_data")
    def test_get_rate_success(self, mock_get_data, test_config, sample_forex_response):
        """Test successful specific currency pair retrieval"""
        mock_get_data.return_value = sample_forex_response

        service = ForexService(test_config)
        result = service.get_rate("USD", "KRW")

        assert isinstance(result, dict)
        assert result["from"] == "USD"
        assert result["to"] == "KRW"
        assert result["rate"] == 1300.0
        assert result["date"] == "2025-01-01"
        assert "timestamp" in result

        mock_get_data.assert_called_once_with("USD")

    @patch.object(ForexService, "get_data")
    def test_get_rate_invalid_from_currency(self, mock_get_data, test_config):
        """Test rate retrieval with invalid from currency"""
        service = ForexService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.get_rate("INVALID", "KRW")

        assert "Invalid currency code: INVALID" in str(exc_info.value)
        mock_get_data.assert_not_called()

    @patch.object(ForexService, "get_data")
    def test_get_rate_invalid_to_currency(self, mock_get_data, test_config):
        """Test rate retrieval with invalid to currency"""
        service = ForexService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.get_rate("USD", "INVALID")

        assert "Invalid currency code: INVALID" in str(exc_info.value)
        mock_get_data.assert_not_called()

    @patch.object(ForexService, "get_data")
    def test_get_rate_currency_not_found(
        self, mock_get_data, test_config, sample_forex_response
    ):
        """Test rate retrieval when target currency is not in rates"""
        mock_get_data.return_value = sample_forex_response

        service = ForexService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_rate("USD", "XYZ")

        assert "Exchange rate not found for USD to XYZ" in str(exc_info.value)

    @patch.object(ForexService, "get_data")
    def test_get_major_pairs_success(
        self, mock_get_data, test_config, sample_forex_response
    ):
        """Test successful major currency pairs retrieval"""
        mock_get_data.return_value = sample_forex_response

        service = ForexService(test_config)
        result = service.get_major_pairs()

        assert isinstance(result, dict)
        assert result["base"] == "USD"
        assert "rates" in result
        assert "USD/EUR" in result["rates"]
        assert "USD/GBP" in result["rates"]
        assert "USD/JPY" in result["rates"]
        assert "USD/KRW" in result["rates"]
        assert result["rates"]["USD/EUR"] == 0.85

        mock_get_data.assert_called_once_with("USD")

    @patch.object(ForexService, "get_data")
    def test_get_major_pairs_api_error(self, mock_get_data, test_config):
        """Test major pairs retrieval with API error"""
        mock_get_data.side_effect = Exception("API Error")

        service = ForexService(test_config)

        with pytest.raises(APIException) as exc_info:
            service.get_major_pairs()

        assert "Failed to fetch major currency pairs" in str(exc_info.value)

    @patch.object(ForexService, "get_data")
    def test_get_supported_currencies_success(
        self, mock_get_data, test_config, sample_forex_response
    ):
        """Test successful supported currencies retrieval"""
        mock_get_data.return_value = sample_forex_response

        service = ForexService(test_config)
        result = service.get_supported_currencies()

        assert isinstance(result, list)
        assert "USD" in result  # Base currency should be included
        assert "EUR" in result
        assert "KRW" in result
        assert len(result) == 6  # 5 rates + USD

    @patch.object(ForexService, "get_data")
    def test_get_supported_currencies_fallback(self, mock_get_data, test_config):
        """Test supported currencies with fallback to default list"""
        mock_get_data.side_effect = Exception("API Error")

        service = ForexService(test_config)
        result = service.get_supported_currencies()

        assert isinstance(result, list)
        assert "USD" in result
        assert "EUR" in result
        assert "KRW" in result
        assert len(result) > 10  # Should return default major currencies

    def test_format_symbol_case_conversion(self, test_config):
        """Test symbol formatting converts to uppercase"""
        service = ForexService(test_config)

        assert service._format_symbol("usd") == "USD"
        assert service._format_symbol("  eur  ") == "EUR"
        assert service._format_symbol("krw") == "KRW"

    def test_build_url_with_params(self, test_config):
        """Test URL building with parameters"""
        service = ForexService(test_config)

        base_url = "https://example.com/api"
        params = {"base": "USD", "symbols": "EUR,GBP"}

        url = service._build_url(base_url, params)
        assert "base=USD" in url
        assert "symbols=EUR,GBP" in url

    @patch("requests.get")
    def test_get_data_case_insensitive_currency(
        self, mock_get, test_config, sample_forex_response
    ):
        """Test that currency codes are handled case-insensitively"""
        mock_response = Mock()
        mock_response.json.return_value = sample_forex_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = ForexService(test_config)
        result = service.get_data("usd")  # lowercase

        assert result["base"] == "USD"

        # Check that the URL was called with uppercase
        args, kwargs = mock_get.call_args
        assert "USD" in args[0]
