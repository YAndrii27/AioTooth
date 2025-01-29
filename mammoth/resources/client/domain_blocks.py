from __future__ import annotations
from typing import cast

from .base import BaseClientResource
from ...client import MastodonClient
from ...models import Domain
from ...utils import version
from ...enums import HttpMethods


class DomainBlocks(BaseClientResource):
    def __init__(self, client: MastodonClient) -> None:
        super().__init__(client)

    @version("v1")
    async def get_blocked_domain(
        self: DomainBlocks,
        limit: int
    ) -> list[Domain]:
        session = await self.client(
            HttpMethods.GET,
            "domain_blocks",
            expected_type=Domain,
            response_is_list=True,
            query_parameters={
                "limit": limit
            }
        )
        return cast(list[Domain], await session())

    @version("v1")
    async def block_domain(self: DomainBlocks, domain: str) -> None:
        session = await self.client(
            HttpMethods.POST,
            "domain_blocks",
            expected_type=Domain,
            response_is_list=True,
            post_data={
                "domain": domain
            }
        )
        return cast(None, await session())

    @version("v1")
    async def unblock_domain(self, domain: str) -> None:
        session = await self.client(
            HttpMethods.DELETE,
            "domain_blocks",
            expected_type=Domain,
            response_is_list=True,
            post_data={
                "domain": domain
            }
        )
        return cast(None, await session())
