from __future__ import annotations
from typing import cast

from .base import BaseClientResource
from ...client import MastodonClient
from ...models import Account
from ...utils import version
from ...enums import HttpMethods


class Mutes(BaseClientResource):
    def __init__(self, client: MastodonClient) -> None:
        super().__init__(client)

    @version("v1")
    async def mutes(
        self: BaseClientResource,
        limit: int
    ) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "mutes",
            expected_type=Account,
            response_is_list=True,
            query_parameters={
                "limit": limit
            }
        )
        return cast(list[Account], await session())
