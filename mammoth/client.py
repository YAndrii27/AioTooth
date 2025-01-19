from __future__ import annotations
from functools import cached_property
import httpx

from .resources.client import Accounts, Statuses, Profiles

from .base import BaseInteractor


class MastodonClient(BaseInteractor):

    def __init__(
            self: MastodonClient,
            instance_url: str,
            api_version: str,
            account_token: str,
            httpx_session: httpx.AsyncClient | None = None
    ):
        super().__init__(
            instance_url=instance_url,
            api_version=api_version,
            token=account_token,
            httpx_session=httpx_session,
        )

    @cached_property
    def account(self: MastodonClient):
        return Accounts(self)

    @cached_property
    def profile(self: MastodonClient):
        return Profiles(self)

    @cached_property
    def statuses(self: MastodonClient):
        return Statuses(self)
