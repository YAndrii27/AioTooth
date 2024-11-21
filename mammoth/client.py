from __future__ import annotations
from typing import Optional, Any, Union
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
from .resources.accounts import Accounts
from .enums import HttpMethods

query_param_values = Union[str, list[str], bool, int]
post_data_values = Union[
    str,
    bool,
    list[str],
    bytes,
    dict[str, Any],
    BaseModel,
    list[BaseModel],
    dict[str, BaseModel],
    None
]


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

        self.account = Accounts(self)

    async def __call__(
            self: MastodonClient,
            http_method: HttpMethods,
            scope: str,
            method: str = "",
            url_parameters: Optional[tuple[str, ...]] = None,
            query_parameters: Optional[dict[str, query_param_values]] = None,
            post_data: Optional[dict[str, post_data_values]] = None,
            files: Optional[dict[str, bytes]] = None
    ) -> dict[str, Any]:
        _url_parameters: str = ""

        if url_parameters:
            _url_parameters = "/".join(url_parameters)

        full_url: str = "/".join((
            self.api_url,
            scope,
            method,
            _url_parameters,
        ))

        response = await self.session.request(
            http_method.value,
            full_url,
            headers=self.headers,
            params=query_parameters,
            data=post_data,
            files=files,
        )

        if response.is_success:
            return response.json()

        raise self.exceptions.get(
            response.status_code,
            ApiException
        )(response.json().get("error"))
