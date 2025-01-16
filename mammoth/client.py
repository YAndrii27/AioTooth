from __future__ import annotations
from functools import cached_property
from typing import Optional, Any, Union, TypeVar, Type, overload, Literal
from pydantic import BaseModel
import httpx

from ._exceptions import (
    Forbidden,
    Unauthorized,
    NotFound,
    ApiException,
    UnprocessableEntity,
    ServiceUnavailable
)
from .resources import Accounts, Statuses, Profiles
from .enums import HttpMethods

from .session import Session

query_param_values = Union[str, list[str], bool, int]
post_data_values = Union[
    str,
    int,
    bool,
    list[str],
    bytes,
    dict[str, Any],
    BaseModel,
    list[BaseModel],
    dict[str, BaseModel],
    None,
]

T = TypeVar("T", bound=BaseModel)


class MastodonClient:

    exceptions: dict[int, type[ApiException]] = {
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        422: UnprocessableEntity,
        503: ServiceUnavailable
    }

    def __init__(
            self: MastodonClient,
            instance_url: str,
            api_version: str,
            account_token: str,
            httpx_session: Optional[httpx.AsyncClient] = None
    ):
        self.instance_url = instance_url
        self.api_version = api_version
        self.api_url = f"https://{instance_url}/api/{api_version}"
        self.headers = {
            "Authorization": f"Bearer {account_token}"
        }

        if httpx_session is None:
            httpx_session = httpx.AsyncClient()

        self.session = httpx_session

    @cached_property
    def account(self):
        return Accounts(self)

    @cached_property
    def profile(self):
        return Profiles(self)

    @cached_property
    def statuses(self):
        return Statuses(self)

    def _assemble_url(
        self: MastodonClient,
        scope: str,
        method: str,
        url_parameters: Optional[tuple[str, ...]] = None,
        url_parameters_after_method: bool = False,
    ) -> str:
        _url_parameters: str = ""
        if url_parameters:
            _url_parameters = "/".join(url_parameters)
        if url_parameters_after_method:
            full_url: str = "/".join(
                filter(
                    None,
                    (
                        self.api_url,
                        scope,
                        method,
                        _url_parameters,
                    )
                )
            )
        else:
            full_url: str = "/".join(
                filter(
                    None,
                    (
                        self.api_url,
                        scope,
                        _url_parameters,
                        method,
                    )
                )
            )
        return full_url

    def _validate_response(
        self: MastodonClient,
        response_json: Any,
        expected_types: Type[T],
        response_is_list: bool,
    ) -> Union[T, list[T]]:
        if response_is_list:
            parsed_list: list[T] = []
            for item in response_json:
                item: Any
                parsed_list.append(expected_types.model_validate(item))
            return parsed_list
        return expected_types.model_validate(response_json)

    @overload
    async def __call__(
        self: MastodonClient,
        http_method: HttpMethods,
        scope: str,
        expected_type: Type[T],
        method: str = "",
        url_parameters: Optional[tuple[str, ...]] = None,
        query_parameters: Optional[dict[str, query_param_values]] = None,
        post_data: Optional[dict[str, post_data_values]] = None,
        files: Optional[dict[str, bytes]] = None,
        custom_headers: Optional[dict[str, str]] = None,
        url_parameters_after_method: bool = False,
        response_is_list: Literal[True] = True,
    ) -> Session[T]: ...

    @overload
    async def __call__(
        self: MastodonClient,
        http_method: HttpMethods,
        scope: str,
        expected_type: Type[T],
        method: str = "",
        url_parameters: Optional[tuple[str, ...]] = None,
        query_parameters: Optional[dict[str, query_param_values]] = None,
        post_data: Optional[dict[str, post_data_values]] = None,
        files: Optional[dict[str, bytes]] = None,
        custom_headers: Optional[dict[str, str]] = None,
        url_parameters_after_method: bool = False,
        response_is_list: Literal[False] = False,
    ) -> Session[T]: ...

    async def __call__(
            self: MastodonClient,
            http_method: HttpMethods,
            scope: str,
            expected_type: Type[T],
            method: str = "",
            url_parameters: Optional[tuple[str, ...]] = None,
            query_parameters: Optional[dict[str, query_param_values]] = None,
            post_data: Optional[dict[str, post_data_values]] = None,
            files: Optional[dict[str, bytes]] = None,
            custom_headers: Optional[dict[str, str]] = None,
            url_parameters_after_method: bool = False,
            response_is_list: bool = False,
    ) -> Session[T]:
        url = self._assemble_url(
            scope=scope,
            method=method,
            url_parameters=url_parameters,
            url_parameters_after_method=url_parameters_after_method
        )

        headers = {**self.headers, **(custom_headers or {})}

        return Session[expected_type](
            expected_type=expected_type,
            httpx_session=self.session,
            http_method=http_method.value,
            url=url,
            headers=headers,
            params=query_parameters,
            data=post_data,
            files=files,
            response_is_list=response_is_list
        )
