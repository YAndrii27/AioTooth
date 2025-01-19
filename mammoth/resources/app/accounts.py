from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...app import MastodonApp

from .base import BaseAppResource
from ...enums import HttpMethods
from ...models import Token


class Accounts(BaseAppResource):
    def __init__(self, app: "MastodonApp") -> None:
        super().__init__(app)

    async def register(
            self: Accounts,
            username: str,
            email: str,
            password: str,
            agreement: bool,
            locale: str,
            reason: str | None,
    ) -> None:
        await self.app(
            http_method=HttpMethods.POST,
            scope="accounts",
            expected_type=Token,
            post_data={
                "username": username,
                "email": email,
                "password": password,
                "agreement": agreement,
                "locale": locale,
                "reason": reason,
            },
        )
