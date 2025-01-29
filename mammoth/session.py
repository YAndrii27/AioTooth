from __future__ import annotations
from typing import Any, TypeVar
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

T = TypeVar("T", BaseModel, None)


class Session[T]:

    exceptions: dict[int, type[ApiException]] = {
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        422: UnprocessableEntity,
        503: ServiceUnavailable
    }

    def __init__(
            self,
            expected_type: type[T] | None,
            httpx_session: httpx.AsyncClient,
            http_method: str,
            url: str,
            headers: dict[str, str],
            params: dict[str, query_param_values] | None = None,
            data: dict[str, post_data_values] | None = None,
            files: dict[str, bytes] | None = None,
            response_is_list: bool = False,
    ) -> None:
        self.httpx_session = httpx_session
        self.http_method = http_method
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.files = files
        self.response_is_list = response_is_list
        self.expected = expected_type

    def _validate_response(
        self,
        response_json: Any,
        response_is_list: bool,
    ) -> T | list[T] | None:
        if self.expected is BaseModel:
            if response_is_list:
                parsed_list: list[T] = []
                for item in response_json:
                    item: Any
                    validated_model = self.expected.model_validate(item)
                    parsed_list.append(validated_model)
                return parsed_list
            return self.expected.model_validate(response_json)

    async def __call__(
            self,
    ) -> T | list[T] | None:
        response = await self.httpx_session.request(
            self.http_method,
            self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            files=self.files,
        )
        response_as_json: Any = response.json()  # TODO: make a proper typehint

        if response.is_success:
            return self._validate_response(
                response_as_json,
                self.response_is_list
            )

        error_message = response_as_json.get("error")
        exception_class = self.exceptions.get(
            response.status_code,
            ApiException
        )
        raise exception_class(error_message)
