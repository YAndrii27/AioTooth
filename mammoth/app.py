from __future__ import annotations
from functools import cached_property
import httpx

from .base import BaseInteractor
from .resources.app import Accounts


class MastodonApp(BaseInteractor):
    def __init__(
            self: MastodonApp,
            instance_url: str,
            api_version: str,
            application_token: str,
            httpx_session: httpx.AsyncClient | None = None
    ) -> None:
        super().__init__(
            instance_url=instance_url,
            api_version=api_version,
            token=application_token,
            httpx_session=httpx_session
        )

    @cached_property
    def accounts(self):
        return Accounts(self)
