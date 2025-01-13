from __future__ import annotations
from typing import TYPE_CHECKING, cast

from ..enums import HttpMethods
from ..models import CredentialAccount
from .base import BaseAPI
if TYPE_CHECKING:
    from ..client import MastodonClient


class Profiles(BaseAPI):
    def __init__(self, client: "MastodonClient") -> None:
        super().__init__(client)

    async def delete_avatar(self: Profiles) -> CredentialAccount:
        session = await self.client(
            HttpMethods.DELETE,
            "profile",
            CredentialAccount,
            "avatar",
            response_is_list=False,
        )
        return cast(CredentialAccount, await session())

    async def delete_header(self: Profiles) -> CredentialAccount:
        session = await self.client(
            HttpMethods.DELETE,
            "profile",
            CredentialAccount,
            "header",
            response_is_list=False,
        )
        return cast(CredentialAccount, await session())
