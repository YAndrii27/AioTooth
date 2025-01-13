from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

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
            visibility: Optional[StatusVisibility | str] = None,
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

        headers: dict[str, str] = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        assert not isinstance(visibility, StatusVisibility)

        if scheduled_at is None:
            session = await self.client(
                HttpMethods.POST,
                "statuses",
                Status,
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
            return cast(Status, await session())
        session = await self.client(
            HttpMethods.POST,
            "statuses",
            ScheduledStatus,
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
        return cast(ScheduledStatus, await session())

    async def get_status(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            Status,
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(Status, await session())

    async def get_many_statuses(
            self: Statuses,
            ids: list[str],
    ) -> list[Status]:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            Status,
            query_parameters={"ids": ids},
            response_is_list=True,
        )
        return cast(list[Status], await session())

    async def delete(self: Statuses, id: str) -> Status:
        session = await self.client(
            HttpMethods.DELETE,
            "statuses",
            url_parameters=(id,),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def get_context(self: Statuses, id: str) -> Context:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "context",),
            expected_type=Context,
            response_is_list=False,
        )
        return cast(Context, await session())

    async def translate(self: Statuses, id: str, lang: str) -> Translation:
        session = await self.client(
            HttpMethods.POST,
            "statuses",
            url_parameters=(id, "translate",),
            post_data={"lang": lang},
            expected_type=Translation,
            response_is_list=False,
        )
        return cast(Translation, await session())

    async def reblogged_by(
            self: Statuses,
            id: str,
            limit: int
    ) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "reblogged_by",),
            query_parameters={"limit": limit},
            expected_type=Account,
            response_is_list=True,
        )
        return cast(list[Account], await session())

    async def favourited_by(
            self: Statuses,
            id: str,
            limit: int
    ) -> list[Account]:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "favourited_by",),
            query_parameters={"limit": limit},
            expected_type=Account,
            response_is_list=True,
        )
        return cast(list[Account], await session())

    async def favourite(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "favourite",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def unfavourite(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unfavourite",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def reblog(
            self: Statuses,
            id: str,
            visibility: StatusVisibility
    ) -> Status:
        if visibility == StatusVisibility.DIRECT:
            raise UnprocessableEntity("Status reblog may not be direct")

        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "reblog",),
            post_data={"visibility": visibility.value},
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def unreblog(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unreblog",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def bookmark(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "bookmark",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def unbookmark(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unbookmark",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def mute(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "mute",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def unmute(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unmute",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def pin(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "pin",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def unpin(
            self: Statuses,
            id: str,
    ) -> Status:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            url_parameters=(id, "unpin",),
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

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

        session = await self.client(
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
            expected_type=Status,
            response_is_list=False,
        )
        return cast(Status, await session())

    async def history(
            self: Statuses,
            id: str
    ) -> list[StatusEdit]:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            StatusEdit,
            "history",
            url_parameters=(id,),
            response_is_list=True,
        )
        return cast(list[StatusEdit], await session())

    async def source(
            self: Statuses,
            id: str,
    ) -> StatusSource:
        session = await self.client(
            HttpMethods.GET,
            "statuses",
            StatusSource,
            "source",
            url_parameters=(id,),
            response_is_list=False,
        )
        return cast(StatusSource, await session())
