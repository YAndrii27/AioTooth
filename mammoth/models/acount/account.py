from __future__ import annotations
from pydantic import BaseModel, field_validator
from datetime import datetime

from ..field import Field
from ..custom_emoji import CustomEmoji
from ... import utils


class Account(BaseModel):
    id: int
    username: str | None
    acct: str
    url: str
    display_name: str | None
    note: str | None
    avatar: str | None
    avatar_static: str | None
    header: str | None
    header_static: str | None
    locked: bool
    fields: list[Field]
    emojis: list[CustomEmoji]
    bot: bool
    group: bool
    discoverable: bool | None
    noindex: bool | None
    moved: Account | None = None
    suspended: bool | None = False
    limited: bool | None = False
    created_at: datetime
    last_status_at: str | None
    statuses_count: int
    followers_count: int
    following_count: int

    @field_validator("created_at", mode="before")
    @classmethod
    def parse_date(cls, v: str):
        if isinstance(v, str):  # type: ignore
            return utils.from_string_to_datetime(v)
        raise ValueError(f"{v} is not datetime string")
