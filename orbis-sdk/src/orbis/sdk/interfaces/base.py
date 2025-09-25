from abc import ABC, abstractmethod
from typing import Any, Optional, Union

import pandas as pd

from ..config import Config


class BaseDataService(ABC):
    def __init__(self, config: Optional[Config] = None):
        from ..config import get_config

        self.config = config or get_config()

    @abstractmethod
    def get_data(self, symbol: str, **kwargs) -> Union[pd.DataFrame, dict[str, Any]]:
        pass

    @abstractmethod
    def validate_symbol(self, symbol: str) -> bool:
        pass

    def _format_symbol(self, symbol: str) -> str:
        return symbol.upper().strip()

    def _build_url(self, base_url: str, params: dict[str, Any]) -> str:
        if not params:
            return base_url

        query_string = "&".join(
            [f"{k}={v}" for k, v in params.items() if v is not None]
        )
        return f"{base_url}?{query_string}" if query_string else base_url
