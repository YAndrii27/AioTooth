from __future__ import annotations
from typing import Optional, Any, Union, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ..client import MastodonClient
from .base import BaseAPI

from ..utils import version
from ..enums import HttpMethods
from ..models import (
    Account,
    CredentialAccount,
    AccountWithSource,
    Status,
    AccountsList,
    FeaturedTag,
    FamiliarFollowers,
    Relationship,
    Field
)


query_param_values = Union[str, list[str], bool, int]
post_data_values = Union[str, bool, list[str], bytes, dict[str, Any]]


class Accounts(BaseAPI):

    def __init__(self: Accounts, client: "MastodonClient"):
        super().__init__(client)

    @version("v1")
    async def verify_credentials(self: Accounts) -> CredentialAccount:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            CredentialAccount,
            "verify_credentials"
        )
        # TODO: Think of better ways to ensure types are correct here
        result = cast(CredentialAccount, await session())
        return result

    @version("v1")
    async def update_credentials(
            self: Accounts,
            display_name: Optional[str],
            note: Optional[str],
            avatar: Optional[bytes],
            header: Optional[bytes],
            locked: Optional[bool],
            bot: bool,
            discoverable: bool,
            hide_collections: bool,
            indexable: bool,
            fields_attributes: list[Field],
    ) -> AccountWithSource:

        fields_hash: dict[str, Field] = {}
        for i, v in enumerate(fields_attributes):
            fields_hash[str(i)] = v

        files: dict[str, bytes] = {}

        if avatar:
            files["avatar"] = avatar

        if header:
            files["header"] = header

        session = await self.client(
            HttpMethods.PATCH,
            "accounts",
            AccountWithSource,
            "update_credentials",
            post_data={
                "display_name": display_name,
                "note": note,
                "header": header,
                "locked": locked,
                "bot": bot,
                "discoverable": discoverable,
                "hide_collections": hide_collections,
                "indexable": indexable,
                "fields_attributes": fields_hash,
            },
            files=files,
            response_is_list=False
        )
        result = cast(AccountWithSource, await session())
        return result

    @version("v1")
    async def get_account(self: Accounts, id: str) -> Account:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            expected_type=Account,
            url_parameters=(id,),
            response_is_list=False
        )
        result = cast(Account, await session())
        return result

    @version("v1")
    async def get_accounts(
        self: Accounts,
        ids: list[str]
    ) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            query_parameters={"id": ids},
            expected_type=Account,
            response_is_list=True
        )
        result = cast(list[Account], await session())
        return result

    @version("v1")
    async def get_statuses(self: Accounts, id: str) -> list[Status]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Status,
            "statuses",
            url_parameters_after_method=False,
            url_parameters=(id,),
            response_is_list=True
        )
        return cast(list[Status], await session())

    @version("v1")
    async def get_followers(self: Accounts, id: str) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Account,
            "followers",
            url_parameters=(id,),
            response_is_list=True,
        )
        return cast(list[Account], await session())

    @version("v1")
    async def get_following(self: Accounts, id: str) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Account,
            "following",
            url_parameters=(id,),
            response_is_list=True,
        )
        return cast(list[Account], await session())

    @version("v1")
    async def get_featured_tags(
        self: Accounts,
        id: str
    ) -> list[FeaturedTag]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            FeaturedTag,
            "featured_tags",
            url_parameters=(id,),
        )
        return cast(list[FeaturedTag], await session())

    @version("v1")
    async def get_lists_with_account(
        self: Accounts,
        id: str
    ) -> list[AccountsList]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            AccountsList,
            "lists",
            url_parameters=(id,),
            response_is_list=True
        )
        return cast(list[AccountsList], await session())

    @version("v1")
    async def follow(
            self: Accounts,
            id: str,
            reblogs: bool,
            notify: bool,
            languages: list[str]
    ) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "follow",
            url_parameters=(id,),
            post_data={
                "reblogs": reblogs,
                "notify": notify,
                "languages": languages
            },
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def unfollow(self: Accounts, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "unfollow",
            url_parameters=(id,),
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def remove_from_followers(
        self: Accounts,
        id: str
    ) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "remove_from_followers",
            url_parameters=(id,),
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def block(self: Accounts, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "block",
            url_parameters=(id,),
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def unblock(self: Accounts, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "unblock",
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(Relationship, await session())

    @version("v1")
    async def mute(self: Accounts, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "mute",
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(Relationship, await session())

    @version("v1")
    async def unmute(self: Accounts, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "unmute",
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(Relationship, await session())

    @version("v1")
    async def feature(self, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "pin",
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(Relationship, await session())

    @version("v1")
    async def unfeature(self, id: str) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "unpin",
            url_parameters=(id,),
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def set_private_note(
        self: Accounts,
        id: str,
        comment: str
    ) -> Relationship:
        session = await self.client(
            HttpMethods.POST,
            "accounts",
            Relationship,
            "note",
            url_parameters=(id,),
            post_data={"comment": comment},
            response_is_list=False
        )
        return cast(Relationship, await session())

    @version("v1")
    async def relationships(
        self: Accounts,
        ids: list[str],
        with_suspended: bool
    ) -> list[Relationship]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Relationship,
            "relationships",
            query_parameters={"id": ids, "with_suspended": with_suspended},
            response_is_list=True,
        )
        return cast(list[Relationship], await session())

    @version("v1")
    async def familiar_followers(
            self: Accounts,
            id: list[str]
    ) -> FamiliarFollowers:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            FamiliarFollowers,
            "familiar_followers",
            query_parameters={"id": id},
            response_is_list=False
        )
        return cast(FamiliarFollowers, await session())

    @version("v1")
    async def search(
            self: Accounts,
            query: str,
            offset: int = 0,
            limit: int = 40,
            resolve: bool = False,
            following: bool = False
    ) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Account,
            "search",
            query_parameters={
                "q": query,
                "limit": limit,
                "offset": offset,
                "resolve": resolve,
                "following": following
            },
            response_is_list=True
        )
        return cast(list[Account], await session())

    @version("v1")
    async def lookup(
            self: Accounts,
            acct: str,
    ) -> Account:
        session = await self.client(
            HttpMethods.GET,
            "accounts",
            Account,
            "lookup",
            query_parameters={
                "acct": acct,
            },
            response_is_list=False
        )
        return cast(Account, await session())
