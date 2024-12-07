from typing import TYPE_CHECKING

from ..enums import HttpMethods
from ..models import CredentialAccount
from .base import BaseAPI
if TYPE_CHECKING:
    from ..client import MastodonClient


class Profiles(BaseAPI):
    def __init__(self, client: "MastodonClient") -> None:
        super().__init__(client)

    async def delete_avatar(self):
        _json = await self.client(
            HttpMethods.DELETE,
            "profile",
            "avatar"
        )
        return CredentialAccount.model_validate(_json)

    async def delete_header(self):
        _json = await self.client(
            HttpMethods.DELETE,
            "profile",
            "header"
        )
        return CredentialAccount.model_validate(_json)
