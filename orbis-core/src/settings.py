from __future__ import annotations

import logging
import os
import json
from typing import TYPE_CHECKING, Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession as SAAsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker


if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

    from orbis.api.common.types import UIAlert

log = logging.getLogger(__name__)

Session: scoped_session
NonScopedSession: sessionmaker
AsyncSession: Callable[..., SAAsyncSession]
