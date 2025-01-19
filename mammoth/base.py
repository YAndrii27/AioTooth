from __future__ import annotations
from typing import Optional, Any, TypeVar, Union
from pydantic import BaseModel
import httpx

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


class BaseInteractor:
    def __init__(
            self,
            instance_url: str,
            api_version: str,
            token: str,
            httpx_session: Optional[httpx.AsyncClient] = None
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
        self: BaseInteractor,
        response_json: Any,
        expected_types: type[T],
        response_is_list: bool,
    ) -> T | list[T]:
        if response_is_list:
            parsed_list: list[T] = []
            for item in response_json:
                item: Any
                parsed_list.append(expected_types.model_validate(item))
            return parsed_list
        return expected_types.model_validate(response_json)

    async def __call__(
            self: BaseInteractor,
            http_method: HttpMethods,
            scope: str,
            expected_type: type[T],
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
