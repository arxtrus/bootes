"""
Integration tests for bootes SDK

These tests verify that the main SDK class works correctly with all services.
Note: These tests use mocking to avoid making real API calls during testing.
"""

from unittest.mock import Mock, patch

import pandas as pd
import pytest
from bootes.sdk import BootesSDK, Config
from bootes.sdk.exceptions import BootesSDKException
from bootes.sdk.services import CryptoService, ForexService, StockService


class TestBootesSDK:
    def test_sdk_initialization_default(self):
        """Test SDK initialization with default config"""
        sdk = BootesSDK()

        assert sdk.config is not None
        assert isinstance(sdk.config, Config)
        # Services should be lazy-loaded (None until accessed)
        assert sdk._stock is None
        assert sdk._forex is None
        assert sdk._crypto is None

    def test_sdk_initialization_custom_config(self, test_config):
        """Test SDK initialization with custom config"""
        sdk = BootesSDK(test_config)

        assert sdk.config is test_config
        assert sdk.config.timeout == 10  # From test_config fixture

    def test_sdk_stock_property_lazy_loading(self, test_config):
        """Test that stock service is lazy-loaded"""
        sdk = BootesSDK(test_config)

        assert sdk._stock is None
        stock_service = sdk.stock
        assert isinstance(stock_service, StockService)
        assert sdk._stock is stock_service
        assert stock_service.config is test_config

        # Second access should return same instance
        assert sdk.stock is stock_service

    def test_sdk_forex_property_lazy_loading(self, test_config):
        """Test that forex service is lazy-loaded"""
        sdk = BootesSDK(test_config)

        assert sdk._forex is None
        forex_service = sdk.forex
        assert isinstance(forex_service, ForexService)
        assert sdk._forex is forex_service
        assert forex_service.config is test_config

        # Second access should return same instance
        assert sdk.forex is forex_service

    def test_sdk_crypto_property_lazy_loading(self, test_config):
        """Test that crypto service is lazy-loaded"""
        sdk = BootesSDK(test_config)

        assert sdk._crypto is None
        crypto_service = sdk.crypto
        assert isinstance(crypto_service, CryptoService)
        assert sdk._crypto is crypto_service
        assert crypto_service.config is test_config

        # Second access should return same instance
        assert sdk.crypto is crypto_service

    def test_sdk_all_services_share_config(self, test_config):
        """Test that all services share the same config"""
        sdk = BootesSDK(test_config)

        stock_service = sdk.stock
        forex_service = sdk.forex
        crypto_service = sdk.crypto

        assert stock_service.config is test_config
        assert forex_service.config is test_config
        assert crypto_service.config is test_config


class TestSDKIntegration:
    @patch("requests.get")
    def test_sdk_stock_integration(self, mock_get, test_config, sample_yahoo_response):
        """Test SDK stock service integration"""
        mock_response = Mock()
        mock_response.json.return_value = sample_yahoo_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        sdk = BootesSDK(test_config)
        result = sdk.stock.get_data("AAPL")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert "symbol" in result.columns
        assert result["symbol"].iloc[0] == "AAPL"

    @patch("requests.get")
    def test_sdk_forex_integration(self, mock_get, test_config, sample_forex_response):
        """Test SDK forex service integration"""
        mock_response = Mock()
        mock_response.json.return_value = sample_forex_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        sdk = BootesSDK(test_config)
        result = sdk.forex.get_data("USD")

        assert isinstance(result, dict)
        assert result["base"] == "USD"
        assert "rates" in result
        assert result["rates"]["KRW"] == 1300.0

    @patch("requests.get")
    def test_sdk_crypto_integration(
        self, mock_get, test_config, sample_crypto_price_response
    ):
        """Test SDK crypto service integration"""
        mock_response = Mock()
        mock_response.json.return_value = sample_crypto_price_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        sdk = BootesSDK(test_config)
        result = sdk.crypto.get_data("bitcoin")

        assert isinstance(result, dict)
        assert result["symbol"] == "bitcoin"
        assert result["price"] == 45000.0
        assert result["vs_currency"] == "usd"

    @patch("requests.get")
    def test_sdk_multiple_service_calls(
        self,
        mock_get,
        test_config,
        sample_yahoo_response,
        sample_forex_response,
        sample_crypto_price_response,
    ):
        """Test multiple service calls with the same SDK instance"""

        def mock_response_side_effect(url, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            if "finance.yahoo.com" in url:
                mock_response.json.return_value = sample_yahoo_response
            elif "exchangerate-api.com" in url:
                mock_response.json.return_value = sample_forex_response
            elif "coingecko.com" in url:
                mock_response.json.return_value = sample_crypto_price_response

            return mock_response

        mock_get.side_effect = mock_response_side_effect

        sdk = BootesSDK(test_config)

        # Test all services
        stock_result = sdk.stock.get_data("AAPL")
        forex_result = sdk.forex.get_data("USD")
        crypto_result = sdk.crypto.get_data("bitcoin")

        # Verify results
        assert isinstance(stock_result, pd.DataFrame)
        assert isinstance(forex_result, dict)
        assert isinstance(crypto_result, dict)

        assert stock_result["symbol"].iloc[0] == "AAPL"
        assert forex_result["base"] == "USD"
        assert crypto_result["symbol"] == "bitcoin"

        # Verify all services use same config
        assert sdk.stock.config is sdk.forex.config is sdk.crypto.config

    def test_sdk_exception_propagation(self, test_config):
        """Test that service exceptions are properly propagated through SDK"""
        sdk = BootesSDK(test_config)

        # Test invalid symbol validation
        with pytest.raises(BootesSDKException):
            sdk.stock.get_data("INVALID$SYMBOL")

        with pytest.raises(BootesSDKException):
            sdk.forex.get_data("INVALID")

        with pytest.raises(BootesSDKException):
            sdk.crypto.get_data("invalid$symbol")


class TestEndToEndWorkflows:
    @patch("requests.get")
    def test_portfolio_tracking_workflow(
        self,
        mock_get,
        test_config,
        sample_yahoo_response,
        sample_forex_response,
        sample_crypto_price_response,
    ):
        """Test a portfolio tracking workflow using multiple services"""

        def mock_response_side_effect(url, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            if "finance.yahoo.com" in url:
                if "quote" in url:
                    mock_response.json.return_value = {
                        "quoteResponse": {
                            "result": [
                                {
                                    "symbol": "AAPL",
                                    "regularMarketPrice": 150.0,
                                    "currency": "USD",
                                }
                            ]
                        }
                    }
                else:
                    mock_response.json.return_value = sample_yahoo_response
            elif "exchangerate-api.com" in url:
                mock_response.json.return_value = sample_forex_response
            elif "coingecko.com" in url:
                mock_response.json.return_value = sample_crypto_price_response

            return mock_response

        mock_get.side_effect = mock_response_side_effect

        sdk = BootesSDK(test_config)

        # Simulate portfolio tracking workflow
        portfolio = []

        # Get stock quote
        stock_quote = sdk.stock.get_quote("AAPL")
        portfolio.append(
            {
                "type": "stock",
                "symbol": "AAPL",
                "price_usd": stock_quote["regularMarketPrice"],
            }
        )

        # Get crypto price
        crypto_data = sdk.crypto.get_data("bitcoin")
        portfolio.append(
            {"type": "crypto", "symbol": "bitcoin", "price_usd": crypto_data["price"]}
        )

        # Get exchange rate for portfolio value in KRW
        forex_data = sdk.forex.get_rate("USD", "KRW")
        usd_to_krw = forex_data["rate"]

        # Calculate portfolio value in both USD and KRW
        total_usd = sum(item["price_usd"] for item in portfolio)
        total_krw = total_usd * usd_to_krw

        # Assertions
        assert len(portfolio) == 2
        assert portfolio[0]["type"] == "stock"
        assert portfolio[1]["type"] == "crypto"
        assert total_usd == 150.0 + 45000.0  # AAPL + Bitcoin
        assert total_krw == total_usd * 1300.0  # USD to KRW rate

    @patch("requests.get")
    def test_market_analysis_workflow(
        self, mock_get, test_config, sample_crypto_top_response, sample_yahoo_response
    ):
        """Test a market analysis workflow"""

        def mock_response_side_effect(url, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            if "coingecko.com" in url and "markets" in url:
                mock_response.json.return_value = sample_crypto_top_response
            elif "finance.yahoo.com" in url:
                mock_response.json.return_value = sample_yahoo_response

            return mock_response

        mock_get.side_effect = mock_response_side_effect

        sdk = BootesSDK(test_config)

        # Market analysis workflow
        analysis = {}

        # Get top cryptocurrencies
        top_cryptos = sdk.crypto.get_top_cryptos(limit=5)
        analysis["crypto_leaders"] = top_cryptos

        # Get stock data for comparison
        stock_data = sdk.stock.get_data("AAPL", period="1mo")
        analysis["stock_performance"] = {
            "symbol": "AAPL",
            "data_points": len(stock_data),
            "latest_close": (
                stock_data["close"].iloc[-1] if len(stock_data) > 0 else None
            ),
        }

        # Verify analysis results
        assert "crypto_leaders" in analysis
        assert "stock_performance" in analysis
        assert len(analysis["crypto_leaders"]) == 2  # From sample data
        assert analysis["crypto_leaders"][0]["id"] == "bitcoin"
        assert analysis["stock_performance"]["symbol"] == "AAPL"

    def test_sdk_metadata_access(self):
        """Test SDK metadata and version information"""
        from bootes.sdk import __author__, __email__, __version__

        assert __version__ == "0.1.0"
        assert __author__ == "arxtrus bootes team"
        assert __email__ == "bootes@arxtrus.com"

    def test_sdk_exports(self):
        """Test that SDK exports all necessary classes and functions"""
        from bootes.sdk import (
            APIException,
            BootesSDK,
            BootesSDKException,
            Config,
            CryptoService,
            DataNotFoundException,
            ForexService,
            NetworkException,
            RateLimitException,
            StockService,
            ValidationException,
            get_config,
        )

        # Verify all classes are importable
        assert BootesSDK is not None
        assert StockService is not None
        assert ForexService is not None
        assert CryptoService is not None
        assert Config is not None
        assert get_config is not None
        assert BootesSDKException is not None
        assert APIException is not None
        assert DataNotFoundException is not None
        assert RateLimitException is not None
        assert ValidationException is not None
        assert NetworkException is not None
