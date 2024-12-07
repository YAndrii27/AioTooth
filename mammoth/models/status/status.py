from typing import Optional, Self
from pydantic import BaseModel
from datetime import datetime

from ...enums.status_visibility import StatusVisibility
from ..preview.preview_card import PreviewCard
from ..poll import Poll
from ..custom_emoji import CustomEmoji
from . import StatusMentions, StatusTag
from ..acount import Account
from ..filter_result import FilterResult


class Status(BaseModel):
    id: str
    uri: str
    created_at: datetime
    account: Account
    content: str
    visibility: StatusVisibility
    sensitive: bool
    spoiler_text: Optional[str]
    media_attachments: list[str]
    application: Optional[dict[str, str | None]]
    mentions: list[StatusMentions]
    tags: list[StatusTag]
    emojis: list[CustomEmoji]
    reblogs_count: int
    favourites_count: int
    replies_count: int
    url: Optional[str]
    in_reply_to_id: Optional[str]
    in_reply_to_account_id: Optional[str]
    reblog: Optional[Self]
    poll: Optional[Poll]
    card: Optional[PreviewCard]
    language: Optional[str]
    text: Optional[str] = None
    edited_at: Optional[datetime]
    favourited: Optional[bool]
    reblogged: Optional[bool]
    muted: Optional[bool]
    bookmarked: Optional[bool]
    pinned: Optional[bool]
    filtered: Optional[list[FilterResult]]
