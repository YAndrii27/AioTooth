from __future__ import annotations
from typing import cast

from .base import BaseClientResource
from ...client import MastodonClient
from ...models import Status
from ...utils import version
from ...enums import HttpMethods


class Favourites(BaseClientResource):
    def __init__(self, client: MastodonClient) -> None:
        super().__init__(client)

    @version("v1")
    async def favourites(
        self: BaseClientResource,
        limit: int
    ) -> list[Status]:
        session = await self.client(
            HttpMethods.GET,
            "favourites",
            expected_type=Status,
            response_is_list=True,
            query_parameters={
                "limit": limit
            }
        )
        return cast(list[Status], await session())
