from typing import Self
from pydantic import BaseModel
from datetime import datetime

from ...enums.status_visibility import StatusVisibility
from ..preview.preview_card import PreviewCard
from ..poll import Poll
from ..custom_emoji import CustomEmoji
from . import StatusMentions, StatusTag
from ..acount import Account
from ..filter import FilterResult


class Status(BaseModel):
    id: str
    uri: str
    created_at: datetime
    account: Account
    content: str
    visibility: StatusVisibility
    sensitive: bool
    spoiler_text: str | None
    media_attachments: list[str]
    application: dict[str, str | None] | None
    mentions: list[StatusMentions]
    tags: list[StatusTag]
    emojis: list[CustomEmoji]
    reblogs_count: int
    favourites_count: int
    replies_count: int
    url: str | None
    in_reply_to_id: str | None
    in_reply_to_account_id: str | None
    reblog: Self | None
    poll: Poll | None
    card: PreviewCard | None
    language: str | None
    text: str | None = None
    edited_at: datetime | None
    favourited: bool | None
    reblogged: bool | None
    muted: bool | None
    bookmarked: bool | None
    pinned: bool | None
    filtered: list[FilterResult] | None
