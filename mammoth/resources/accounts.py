from __future__ import annotations
from typing import Optional, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MastodonClient
from .base import BaseAPI

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

    async def verify_credentials(self: Accounts) -> CredentialAccount:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            "verify_credentials"
        )
        return CredentialAccount.model_validate(_json)

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

        _json = await self.client(
            HttpMethods.PATCH,
            "accounts",
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
            files=files
        )
        return AccountWithSource.model_validate(_json)

    async def get_account(self: Accounts, id: str) -> Account:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id,)
        )
        return Account.model_validate(_json)

    async def get_accounts(
        self: Accounts,
        ids: list[str]
    ) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            query_parameters={"id": ids}
        )
        return [Account.model_validate(account) for account in _json]

    async def get_statuses(self: Accounts, id: str) -> list[Status]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id, "statuses")
        )
        return [Status.model_validate(status) for status in _json]

    async def get_followers(self: Accounts, id: str) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id, "followers")
        )
        return [Account.model_validate(account) for account in _json]

    async def get_following(self: Accounts, id: str) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id, "following")
        )
        return [Account.model_validate(account) for account in _json]

    async def get_featured_tags(
        self: Accounts,
        id: str
    ) -> list[FeaturedTag]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id, "featured_tags")
        )
        return [FeaturedTag.model_validate(tag) for tag in _json]

    async def get_lists_with_account(
        self: Accounts,
        id: str
    ) -> list[AccountsList]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            url_parameters=(id, "lists")
        )
        accounts_lists: list[AccountsList] = []
        for accounts_list in _json:
            accounts_lists.append(AccountsList.model_validate(accounts_list))
        return accounts_lists

    async def follow(
            self: Accounts,
            id: str,
            reblogs: bool,
            notify: bool,
            languages: list[str]
    ) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "follow"),
            post_data={
                "reblogs": reblogs,
                "notify": notify,
                "languages": languages
            }
        )
        return Relationship.model_validate(_json)

    async def unfollow(self: Accounts, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "unfollow"),
        )
        return Relationship.model_validate(_json)

    async def remove_from_followers(
        self: Accounts,
        id: str
    ) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "remove_from_followers"),
        )
        return Relationship.model_validate(_json)

    async def block(self: Accounts, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "block"),
        )
        return Relationship.model_validate(_json)

    async def unblock(self: Accounts, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "unblock"),
        )
        return Relationship.model_validate(_json)

    async def mute(self: Accounts, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "mute"),
        )
        return Relationship.model_validate(_json)

    async def unmute(self: Accounts, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "unmute"),
        )
        return Relationship.model_validate(_json)

    async def feature(self, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "pin",),
        )
        return Relationship.model_validate(_json)

    async def unfeature(self, id: str) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "unpin"),
        )
        return Relationship.model_validate(_json)

    async def set_private_note(
        self: Accounts,
        id: str,
        comment: str
    ) -> Relationship:
        _json = await self.client(
            HttpMethods.POST,
            "accounts",
            url_parameters=(id, "note"),
            post_data={"comment": comment}
        )
        return Relationship.model_validate(_json)

    async def relationships(
        self: Accounts,
        ids: list[str],
        with_suspended: bool
    ) -> list[Relationship]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            "relationships",
            query_parameters={"id": ids, "with_suspended": with_suspended}
        )
        relationships: list[Relationship] = []
        for relationship in _json:
            relationships.append(
                Relationship.model_validate(relationship)
            )
        return relationships

    async def familiar_followers(
            self: Accounts,
            id: list[str]
    ) -> FamiliarFollowers:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            "familiar_followers",
            query_parameters={"id": id}
        )
        return FamiliarFollowers.model_validate(_json)

    async def search(
            self: Accounts,
            query: str,
            offset: int = 0,
            limit: int = 40,
            resolve: bool = False,
            following: bool = False
    ) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            "search",
            query_parameters={
                "q": query,
                "limit": limit,
                "offset": offset,
                "resolve": resolve,
                "following": following
            }
        )
        accounts_list: list[Account] = []
        for account in _json:
            accounts_list.append(Account.model_validate(account))
        return accounts_list

    async def lookup(
            self: Accounts,
            acct: str,
    ) -> Account:
        _json = await self.client(
            HttpMethods.GET,
            "accounts",
            "lookup",
            query_parameters={
                "acct": acct,
            }
        )
        return Account.model_validate(_json)
