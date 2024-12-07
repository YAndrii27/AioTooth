from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from .base import BaseAPI
from ..enums import StatusVisibility, HttpMethods
from ..models import (
    NewPoll,
    Status,
    ScheduledStatus,
    Context,
    Translation,
    Account,
    StatusEdit,
    StatusSource
)
from .._exceptions import UnprocessableEntity
if TYPE_CHECKING:
    from ..client import MastodonClient


class Statuses(BaseAPI):
    def __init__(self: Statuses, client: "MastodonClient") -> None:
        super().__init__(client)

    async def post(
            self: Statuses,
            status: Optional[str] = None,
            media_ids: Optional[list[str]] = None,
            poll: Optional[NewPoll] = None,
            in_reply_to_id: Optional[int] = None,
            spoiler_text: Optional[str] = None,
            visibility: Optional[StatusVisibility] = None,
            sensitive: Optional[bool] = False,
            language: Optional[str] = None,
            scheduled_at: Optional[datetime | str] = None,
            idempotency_key: Optional[str] = None,
    ) -> Status | ScheduledStatus:
        if all((not status, not media_ids, not poll)):
            raise UnprocessableEntity("Status content may not be empty")

        if isinstance(visibility, StatusVisibility):
            visibility = visibility.value
        if isinstance(scheduled_at, datetime):
            scheduled_at = scheduled_at.strftime("%Y-%m-%d %H:%M:%S")

        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        assert not isinstance(visibility, StatusVisibility)

        _json = await self.client(
            HttpMethods.POST,
            "statuses",
            post_data={
                "status": status,
                "media_ids": media_ids,
                "poll": poll,
                "in_reply_to_id": in_reply_to_id,
                "spoiler_text": spoiler_text,
                "visibility": visibility,
                "sensitive": sensitive,
                "language": language,
            },
            custom_headers=headers
        )

        if scheduled_at is None:
            return Status.model_validate(_json)
        return ScheduledStatus.model_validate(_json)

    async def get_status(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id,)
        )
        return Status.model_validate(_json)

    async def get_many_statuses(
            self: Statuses,
            ids: list[str],
    ) -> list[Status]:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            query_parameters={"ids": ids}
        )
        return [Status.model_validate(status) for status in _json]

    async def delete(self: Statuses, id: str) -> Status:
        _json = await self.client(
            HttpMethods.DELETE,
            "statuses",
            url_parameters=(id,)
        )
        return Status.model_validate(_json)

    async def get_context(self: Statuses, id: str) -> Context:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "context",)
        )
        return Context.model_validate(_json)

    async def translate(self: Statuses, id: str, lang: str) -> Translation:
        _json = await self.client(
            HttpMethods.POST,
            "statuses",
            url_parameters=(id, "translate",),
            post_data={"lang": lang}
        )
        return Translation.model_validate(_json)

    async def reblogged_by(
            self: Statuses,
            id: str,
            limit: int
    ) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "reblogged_by",),
            query_parameters={"limit": limit},
        )
        return [Account.model_validate(account) for account in _json]

    async def favourited_by(
            self: Statuses,
            id: str,
            limit: int
    ) -> list[Account]:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "favourited_by",),
            query_parameters={"limit": limit},
        )
        return [Account.model_validate(account) for account in _json]

    async def favourite(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "favourite",),
        )
        return Status.model_validate(_json)

    async def unfavourite(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unfavourite",),
        )
        return Status.model_validate(_json)

    async def reblog(
            self: Statuses,
            id: str,
            visibility: StatusVisibility
    ) -> Status:
        if visibility.value == StatusVisibility.DIRECT:
            raise UnprocessableEntity("Status reblog may not be direct")

        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "reblog",),
            post_data=visibility.value,
        )
        return Status.model_validate(_json)

    async def unreblog(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unreblog",),
        )
        return Status.model_validate(_json)

    async def bookmark(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "bookmark",),
        )
        return Status.model_validate(_json)

    async def unbookmark(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unbookmark",),
        )
        return Status.model_validate(_json)

    async def mute(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "mute",),
        )
        return Status.model_validate(_json)

    async def unmute(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unmute",),
        )
        return Status.model_validate(_json)

    async def pin(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "pin",),
        )
        return Status.model_validate(_json)

    async def unpin(
            self: Statuses,
            id: str,
    ) -> Status:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unpin",),
        )
        return Status.model_validate(_json)

    async def edit(
            self: Statuses,
            status: Optional[str] = None,
            media_ids: Optional[list[str]] = None,
            media_attributes: Optional[list[str]] = None,
            poll: Optional[NewPoll] = None,
            in_reply_to_id: Optional[int] = None,
            spoiler_text: Optional[str] = None,
            visibility: Optional[StatusVisibility | str] = None,
            sensitive: Optional[bool] = False,
            language: Optional[str] = None,
    ) -> Status:
        if isinstance(visibility, StatusVisibility):
            visibility = visibility.value

        assert not isinstance(visibility, StatusVisibility)

        _json = await self.client(
            HttpMethods.PUT,
            "statuses",
            post_data={
                "status": status,
                "media_ids": media_ids,
                "media_attributes": media_attributes,
                "poll": poll,
                "in_reply_to_id": in_reply_to_id,
                "spoiler_text": spoiler_text,
                "visibility": visibility,
                "sensitive": sensitive,
                "language": language,
            },
        )
        return Status.model_validate(_json)

    async def history(
            self: Statuses,
            id: str
    ) -> list[StatusEdit]:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "history",),
        )
        return [StatusEdit.model_validate(status_edit) for status_edit in _json]

    async def source(
            self: Statuses,
            id: str,
    ) -> StatusSource:
        _json = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "source",),
        )
        return StatusSource.model_validate(_json)
