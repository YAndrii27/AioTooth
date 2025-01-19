from __future__ import annotations
from typing import TYPE_CHECKING, cast

from ...enums import HttpMethods
from ...models import CredentialAccount
from ...utils import version
from .base import BaseClientResource
if TYPE_CHECKING:
    from ...client import MastodonClient


class Profiles(BaseClientResource):
    def __init__(self, client: "MastodonClient") -> None:
        super().__init__(client)

    @version("v1")
    async def delete_avatar(self: Profiles) -> CredentialAccount:
        session = await self.client(
            HttpMethods.DELETE,
            "profile",
            CredentialAccount,
            "avatar",
            response_is_list=False,
        )
        return cast(CredentialAccount, await session())

    @version("v1")
    async def delete_header(self: Profiles) -> CredentialAccount:
        session = await self.client(
            HttpMethods.DELETE,
            "profile",
            CredentialAccount,
            "header",
            response_is_list=False,
        )
        return cast(CredentialAccount, await session())
