"""
Tests for Config module
"""

import os
from unittest.mock import patch

import pytest
from orbis.sdk.config import Config, get_config


class TestConfig:
    def test_config_default_values(self):
        """Test Config with default values"""
        config = Config()

        assert config.alpha_vantage_key is None
        assert config.finnhub_key is None
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.default_stock_interval == "1d"
        assert config.default_stock_period == "1y"
        assert config.cache_enabled is False
        assert config.cache_ttl == 300
        assert config.requests_per_minute == 60

    def test_config_custom_values(self):
        """Test Config with custom values"""
        config = Config(
            alpha_vantage_key="test_av_key",
            finnhub_key="test_fh_key",
            timeout=60,
            max_retries=5,
            retry_delay=2.0,
            default_stock_interval="5m",
            default_stock_period="6mo",
            cache_enabled=True,
            cache_ttl=600,
            requests_per_minute=120,
        )

        assert config.alpha_vantage_key == "test_av_key"
        assert config.finnhub_key == "test_fh_key"
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.default_stock_interval == "5m"
        assert config.default_stock_period == "6mo"
        assert config.cache_enabled is True
        assert config.cache_ttl == 600
        assert config.requests_per_minute == 120

    @patch.dict(
        os.environ,
        {
            "ALPHA_VANTAGE_API_KEY": "env_av_key",
            "FINNHUB_API_KEY": "env_fh_key",
            "ORBIS_TIMEOUT": "45",
            "ORBIS_MAX_RETRIES": "4",
            "ORBIS_RETRY_DELAY": "1.5",
            "ORBIS_DEFAULT_INTERVAL": "15m",
            "ORBIS_DEFAULT_PERIOD": "3mo",
            "ORBIS_CACHE_ENABLED": "true",
            "ORBIS_CACHE_TTL": "450",
            "ORBIS_REQUESTS_PER_MINUTE": "90",
        },
        clear=True,
    )
    def test_config_from_env(self):
        """Test Config.from_env() with environment variables"""
        config = Config.from_env()

        assert config.alpha_vantage_key == "env_av_key"
        assert config.finnhub_key == "env_fh_key"
        assert config.timeout == 45
        assert config.max_retries == 4
        assert config.retry_delay == 1.5
        assert config.default_stock_interval == "15m"
        assert config.default_stock_period == "3mo"
        assert config.cache_enabled is True
        assert config.cache_ttl == 450
        assert config.requests_per_minute == 90

    @patch.dict(os.environ, {"ORBIS_CACHE_ENABLED": "false"}, clear=True)
    def test_config_from_env_cache_disabled(self):
        """Test Config.from_env() with cache disabled"""
        config = Config.from_env()
        assert config.cache_enabled is False

    @patch.dict(os.environ, {"ORBIS_CACHE_ENABLED": "TRUE"}, clear=True)
    def test_config_from_env_cache_enabled_case_insensitive(self):
        """Test Config.from_env() with cache enabled (case insensitive)"""
        config = Config.from_env()
        assert config.cache_enabled is True

    @patch.dict(os.environ, {}, clear=True)
    def test_config_from_env_defaults(self):
        """Test Config.from_env() with no environment variables"""
        config = Config.from_env()

        assert config.alpha_vantage_key is None
        assert config.finnhub_key is None
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.default_stock_interval == "1d"
        assert config.default_stock_period == "1y"
        assert config.cache_enabled is False
        assert config.cache_ttl == 300
        assert config.requests_per_minute == 60

    @patch.dict(os.environ, {"ORBIS_TIMEOUT": "invalid_number"}, clear=True)
    def test_config_from_env_invalid_integer(self):
        """Test Config.from_env() with invalid integer value"""
        with pytest.raises(ValueError):
            Config.from_env()

    @patch.dict(os.environ, {"ORBIS_RETRY_DELAY": "invalid_float"}, clear=True)
    def test_config_from_env_invalid_float(self):
        """Test Config.from_env() with invalid float value"""
        with pytest.raises(ValueError):
            Config.from_env()


class TestGetConfig:
    def teardown_method(self):
        """Reset global config after each test"""
        # Reset the global _config variable
        from orbis.sdk.config import config as config_module

        config_module._config = None

    def test_get_config_singleton(self):
        """Test that get_config returns singleton instance"""
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2
        assert isinstance(config1, Config)

    @patch.dict(os.environ, {"ORBIS_TIMEOUT": "90"}, clear=True)
    def test_get_config_uses_env(self):
        """Test that get_config uses environment variables"""
        config = get_config()
        assert config.timeout == 90

    @patch("orbis.sdk.config.config.Config.from_env")
    def test_get_config_calls_from_env(self, mock_from_env):
        """Test that get_config calls Config.from_env()"""
        mock_config = Config()
        mock_from_env.return_value = mock_config

        result = get_config()

        mock_from_env.assert_called_once()
        assert result is mock_config

    def test_get_config_caches_result(self):
        """Test that get_config caches the result"""
        with patch("orbis.sdk.config.config.Config.from_env") as mock_from_env:
            mock_config = Config()
            mock_from_env.return_value = mock_config

            # First call
            result1 = get_config()
            # Second call
            result2 = get_config()

            # Should only call from_env once
            mock_from_env.assert_called_once()
            assert result1 is result2

    def test_config_validation_types(self):
        """Test that Config validates types properly"""
        # Test with valid types
        config = Config(
            timeout=30,
            max_retries=3,
            retry_delay=1.0,
            cache_enabled=True,
            cache_ttl=300,
            requests_per_minute=60,
        )

        assert isinstance(config.timeout, int)
        assert isinstance(config.max_retries, int)
        assert isinstance(config.retry_delay, float)
        assert isinstance(config.cache_enabled, bool)
        assert isinstance(config.cache_ttl, int)
        assert isinstance(config.requests_per_minute, int)

    def test_config_string_fields(self):
        """Test Config string fields"""
        config = Config(
            alpha_vantage_key="test_key",
            finnhub_key="another_key",
            default_stock_interval="5m",
            default_stock_period="1mo",
        )

        assert config.alpha_vantage_key == "test_key"
        assert config.finnhub_key == "another_key"
        assert config.default_stock_interval == "5m"
        assert config.default_stock_period == "1mo"

    def test_config_none_values(self):
        """Test Config with None values for optional fields"""
        config = Config(alpha_vantage_key=None, finnhub_key=None)

        assert config.alpha_vantage_key is None
        assert config.finnhub_key is None
