from __future__ import annotations
from typing import Any, TYPE_CHECKING, TypeVar
from collections.abc import Callable, Awaitable
from pydantic import BaseModel
from datetime import datetime
from functools import wraps

from ._exceptions import UnmatchedApiVersion

if TYPE_CHECKING:
    from .client import MastodonClient
    from .app import MastodonApp

if TYPE_CHECKING:
    from .resources.client.base import BaseClientResource
    from .resources.app.base import BaseAppResource


T = TypeVar("T", bound=BaseModel)


def from_string_to_datetime(datetime_str: str):
    return datetime.fromisoformat(datetime_str)


def version(version: str):
    def decorator(method: Callable[..., Awaitable[T | list[T] | None]]):
        @wraps(wrapped=method)
        async def wrapper(
            self: "BaseClientResource | BaseAppResource",
            *args: list[Any],
            **kwargs: dict[Any, Any]
        ) -> T | list[T] | None:
            # Because PyRight can't figure types of getattr() out we have to
            # suspend the error using type: ignore
            #
            # TODO think of better ways to implement this
            interactor: MastodonClient | MastodonApp = (getattr(
                self,
                "client",
                None
            ) or getattr(
                self,
                "app",
                None
            ))  # type: ignore
            if interactor and getattr(
                interactor,
                "api_version",
                None
            ) == version:
                return await method(self, *args, **kwargs)
            else:
                raise UnmatchedApiVersion(f"This method requires {version} \
version of API but was called with \
{interactor.api_version}")
        return wrapper
    return decorator
