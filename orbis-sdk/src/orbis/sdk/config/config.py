import os
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    # API Keys (optional - most services will work without them)
    alpha_vantage_key: Optional[str] = None
    finnhub_key: Optional[str] = None

    # Request settings
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

    # Data settings
    default_stock_interval: str = "1d"
    default_stock_period: str = "1y"
    cache_enabled: bool = False
    cache_ttl: int = 300  # 5 minutes

    # Rate limiting
    requests_per_minute: int = 60

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            alpha_vantage_key=os.getenv("ALPHA_VANTAGE_API_KEY"),
            finnhub_key=os.getenv("FINNHUB_API_KEY"),
            timeout=int(os.getenv("ORBIS_TIMEOUT", "30")),
            max_retries=int(os.getenv("ORBIS_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("ORBIS_RETRY_DELAY", "1.0")),
            default_stock_interval=os.getenv("ORBIS_DEFAULT_INTERVAL", "1d"),
            default_stock_period=os.getenv("ORBIS_DEFAULT_PERIOD", "1y"),
            cache_enabled=os.getenv("ORBIS_CACHE_ENABLED", "false").lower() == "true",
            cache_ttl=int(os.getenv("ORBIS_CACHE_TTL", "300")),
            requests_per_minute=int(os.getenv("ORBIS_REQUESTS_PER_MINUTE", "60")),
        )


_config: Optional[Config] = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config
