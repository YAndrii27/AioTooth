from __future__ import annotations
from typing import Callable, Awaitable, Any, TYPE_CHECKING, TypeVar
from pydantic import BaseModel
from datetime import datetime
from functools import wraps

from ._exceptions import UnmarchedApiVersion

if TYPE_CHECKING:
    from .resources.base import BaseAPI


T = TypeVar("T", bound=BaseModel)


def from_string_to_datetime(datetime_str: str):
    return datetime.fromisoformat(datetime_str)


def version(version: str):
    def decorator(method: Callable[..., Awaitable[T | list[T]]]):
        @wraps(method)
        async def wrapper(
            self: "BaseAPI",
            *args: list[Any],
            **kwargs: dict[Any, Any]
        ):
            if getattr(self.client, "api_version") == version:
                await method(*args, **kwargs)
            else:
                raise UnmarchedApiVersion(f"This method requires {version} \
version of API but was called with \
{self.client.api_version}")
        return wrapper
    return decorator
