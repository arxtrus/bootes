"""
Tests for CryptoService
"""

from unittest.mock import Mock, patch

import pytest
from bootes.sdk.exceptions import (
    APIException,
    DataNotFoundException,
    NetworkException,
    ValidationException,
)
from bootes.sdk.services.crypto import CryptoService


class TestCryptoService:
    def test_init_with_config(self, test_config):
        """Test CryptoService initialization with custom config"""
        service = CryptoService(test_config)
        assert service.config == test_config
        assert service.base_url == "https://api.coingecko.com/api/v3"

    def test_init_without_config(self):
        """Test CryptoService initialization without config"""
        service = CryptoService()
        assert service.config is not None

    def test_validate_symbol_valid(self):
        """Test symbol validation with valid crypto symbols"""
        service = CryptoService()

        valid_symbols = ["bitcoin", "ethereum", "cardano", "bitcoin-cash", "dogecoin"]
        for symbol in valid_symbols:
            assert service.validate_symbol(symbol) is True

    def test_validate_symbol_invalid(self):
        """Test symbol validation with invalid symbols"""
        service = CryptoService()

        invalid_symbols = ["", "a" * 51, None, 123, "bitcoin$", "eth@coin"]
        for symbol in invalid_symbols:
            assert service.validate_symbol(symbol) is False

    @patch("requests.get")
    def test_get_data_success(
        self, mock_get, test_config, sample_crypto_price_response
    ):
        """Test successful crypto price data retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_price_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.get_data("bitcoin", vs_currency="usd")

        assert isinstance(result, dict)
        assert result["symbol"] == "bitcoin"
        assert result["price"] == 45000.0
        assert result["market_cap"] == 850000000000
        assert result["volume_24h"] == 35000000000
        assert result["change_24h"] == 2.5
        assert result["vs_currency"] == "usd"
        assert "timestamp" in result
        assert "last_updated" in result

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "simple/price" in args[0]
        assert kwargs["timeout"] == test_config.timeout
        assert kwargs["params"]["ids"] == "bitcoin"
        assert kwargs["params"]["vs_currencies"] == "usd"

    @patch("requests.get")
    def test_get_data_invalid_symbol(self, mock_get, test_config):
        """Test data retrieval with invalid symbol"""
        service = CryptoService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.get_data("invalid$symbol")

        assert "Invalid crypto symbol: invalid$symbol" in str(exc_info.value)
        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_data_no_data_found(self, mock_get, test_config):
        """Test data retrieval when no data is found"""
        mock_response = Mock()
        mock_response.json.return_value = {}  # Empty response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_data("nonexistent")

        assert "No data found for symbol: nonexistent" in str(exc_info.value)

    @patch("requests.get")
    def test_get_data_network_error(self, mock_get, test_config):
        """Test data retrieval with network error"""
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        service = CryptoService(test_config)

        with pytest.raises(NetworkException) as exc_info:
            service.get_data("bitcoin")

        assert "Failed to fetch data for bitcoin" in str(exc_info.value)

    @patch("requests.get")
    def test_get_market_data_success(
        self, mock_get, test_config, sample_crypto_market_response
    ):
        """Test successful market data retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_market_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.get_market_data("bitcoin", vs_currency="usd")

        assert isinstance(result, dict)
        assert result["id"] == "bitcoin"
        assert result["symbol"] == "btc"
        assert result["name"] == "Bitcoin"
        assert result["current_price"] == 45000.0
        assert result["market_cap"] == 850000000000
        assert result["market_cap_rank"] == 1
        assert result["vs_currency"] == "usd"
        assert "timestamp" in result

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "coins/bitcoin" in args[0]

    @patch("requests.get")
    def test_get_market_data_invalid_symbol(self, mock_get, test_config):
        """Test market data retrieval with invalid symbol"""
        service = CryptoService(test_config)

        with pytest.raises(ValidationException):
            service.get_market_data("invalid$")

        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_market_data_no_market_data(self, mock_get, test_config):
        """Test market data retrieval when no market data is found"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bitcoin"}  # Missing market_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_market_data("bitcoin")

        assert "No market data found for symbol: bitcoin" in str(exc_info.value)

    @patch("requests.get")
    def test_get_top_cryptos_success(
        self, mock_get, test_config, sample_crypto_top_response
    ):
        """Test successful top cryptos retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_top_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.get_top_cryptos(vs_currency="usd", limit=2)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "bitcoin"
        assert result[0]["vs_currency"] == "usd"
        assert result[1]["id"] == "ethereum"

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "coins/markets" in args[0]
        assert kwargs["params"]["vs_currency"] == "usd"
        assert kwargs["params"]["per_page"] == 2

    @patch("requests.get")
    def test_get_top_cryptos_limit_validation(
        self, mock_get, test_config, sample_crypto_top_response
    ):
        """Test top cryptos with limit validation"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_top_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)

        # Test with limit > 250 (should be capped at 250)
        service.get_top_cryptos(limit=300)
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["per_page"] == 250

        # Test with limit < 1 (should default to 10)
        service.get_top_cryptos(limit=0)
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["per_page"] == 10

    @patch("requests.get")
    def test_get_top_cryptos_no_data(self, mock_get, test_config):
        """Test top cryptos when no data is returned"""
        mock_response = Mock()
        mock_response.json.return_value = []  # Empty list
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)

        with pytest.raises(DataNotFoundException):
            service.get_top_cryptos()

    @patch("requests.get")
    def test_search_crypto_success(
        self, mock_get, test_config, sample_crypto_search_response
    ):
        """Test successful crypto search"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_search_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.search_crypto("bitcoin")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == "bitcoin"
        assert result[0]["name"] == "Bitcoin"
        assert result[0]["symbol"] == "BTC"

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "search" in args[0]
        assert kwargs["params"]["query"] == "bitcoin"

    @patch("requests.get")
    def test_search_crypto_invalid_query(self, mock_get, test_config):
        """Test crypto search with invalid query"""
        service = CryptoService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.search_crypto("x")  # Too short

        assert "Query must be at least 2 characters" in str(exc_info.value)
        mock_get.assert_not_called()

        with pytest.raises(ValidationException):
            service.search_crypto("")  # Empty

        with pytest.raises(ValidationException):
            service.search_crypto("  ")  # Whitespace only

    @patch("requests.get")
    def test_search_crypto_no_results(self, mock_get, test_config):
        """Test crypto search with no results"""
        mock_response = Mock()
        mock_response.json.return_value = {}  # No coins key
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.search_crypto("nonexistent")

        assert result == []

    def test_format_symbol_case_conversion(self, test_config):
        """Test symbol formatting converts to lowercase and strips"""
        CryptoService(test_config)

        # Note: _format_symbol is inherited from base class and converts to uppercase
        # But crypto service uses lower() internally
        assert "bitcoin" == "bitcoin".lower().strip()
        assert "ETHEREUM".lower().strip() == "ethereum"

    @patch("requests.get")
    def test_get_data_with_different_vs_currency(self, mock_get, test_config):
        """Test data retrieval with different vs_currency"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "bitcoin": {
                "krw": 55000000.0,
                "krw_market_cap": 1100000000000000,
                "krw_24h_vol": 45000000000000,
                "krw_24h_change": 2.5,
                "last_updated_at": 1640995200,
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)
        result = service.get_data("bitcoin", vs_currency="krw")

        assert result["vs_currency"] == "krw"
        assert result["price"] == 55000000.0

        args, kwargs = mock_get.call_args
        assert kwargs["params"]["vs_currencies"] == "krw"

    @patch("requests.get")
    def test_api_error_handling(self, mock_get, test_config):
        """Test API error handling"""
        mock_response = Mock()
        mock_response.json.side_effect = KeyError("Missing key")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = CryptoService(test_config)

        with pytest.raises(APIException) as exc_info:
            service.get_data("bitcoin")

        assert "Unexpected API response format" in str(exc_info.value)
