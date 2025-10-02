from __future__ import annotations

import contextlib
from collections.abc import Callable, Generator
from functools import wraps
from inspect import signature
from typing import TYPE_CHECKING, ParamSpec, TypeVar, cast

from orbis import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session as OrbisSession


@contextlib.contextmanager
def create_session(scope: bool = True) -> Generator[OrbisSession, None, None]:
    if scope:
        Session = getattr(settings, "Session", None)
    else:
        Session = getattr(settings, "NonScopedSession", None)
    if Session is None:
        raise RuntimeError("Session is not initialized")
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextlib.asynccontextmanager
async def create_session_async():
    from orbis.settings import AsyncSession

    async with AsyncSession() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


PS = ParamSpec("PS")
RT = TypeVar("RT")


def find_session_idx(func: Callable[PS, RT]) -> int:
    func_params = signature(func).parameters
    try:
        sesstion_arg_idx = list(func_params).index("session")
    except ValueError:
        raise ValueError(
            f"'session' parameter not found in function {func.__name__}") from None

    return sesstion_arg_idx


def provide_session(func: Callable[PS, RT]) -> Callable[PS, RT]:
    sesstion_arg_idx = find_session_idx(func)

    @wraps(func)
    def wrapper(*args, **kwargs) -> RT:
        if "session" in kwargs or sesstion_arg_idx < len(args):
            return func(*args, **kwargs)
        with create_session() as session:
            return func(*args, session=session, **kwargs)

    return wrapper


NEW_SESSION = SASession = cast("SASession", None)
