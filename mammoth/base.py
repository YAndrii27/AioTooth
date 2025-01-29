from __future__ import annotations
from typing import Any, TypeVar
from pydantic import BaseModel
import httpx

from .enums import HttpMethods
from .session import Session


query_param_values = str | list[str] | bool | int
post_data_values = str \
    | int \
    | bool \
    | list[str] \
    | bytes \
    | dict[str, Any] \
    | BaseModel \
    | list[BaseModel] \
    | dict[str, BaseModel] \
    | None

T = TypeVar("T", bound=BaseModel)


class BaseInteractor:
    def __init__(
            self,
            instance_url: str,
            api_version: str,
            token: str,
            httpx_session: httpx.AsyncClient | None = None
    ) -> None:
        self.instance_url = instance_url
        self.api_version = api_version
        self.api_url = f"https://{instance_url}/api/{api_version}"
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

        if httpx_session is None:
            httpx_session = httpx.AsyncClient()

        self.session = httpx_session

    def _assemble_url(
        self: BaseInteractor,
        scope: str,
        method: str,
        url_parameters: tuple[str, ...] | None = None,
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

    async def __call__(
            self: BaseInteractor,
            http_method: HttpMethods,
            scope: str,
            expected_type: type[T] | None,
            method: str = "",
            url_parameters: tuple[str, ...] | None = None,
            query_parameters: dict[str, query_param_values] | None = None,
            post_data: dict[str, post_data_values] | None = None,
            files: dict[str, bytes] | None = None,
            custom_headers: dict[str, str] | None = None,
            url_parameters_after_method: bool = False,
            response_is_list: bool = False,
    ) -> Session[T | None]:
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
