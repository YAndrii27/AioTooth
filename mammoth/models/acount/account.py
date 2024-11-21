from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

from ..field import Field
from ..custom_emoji import CustomEmoji
from ... import utils


class Account(BaseModel):
    id: int
    username: Optional[str]
    acct: str
    url: str
    display_name: Optional[str]
    note: Optional[str]
    avatar: Optional[str]
    avatar_static: Optional[str]
    header: Optional[str]
    header_static: Optional[str]
    locked: bool
    fields: list[Field]
    emojis: list[CustomEmoji]
    bot: bool
    group: bool
    discoverable: Optional[bool]
    noindex: Optional[bool]
    moved: Optional[Account] = None
    suspended: Optional[bool] = False
    limited: Optional[bool] = False
    created_at: datetime
    last_status_at: Optional[str]
    statuses_count: int
    followers_count: int
    following_count: int

    @field_validator("created_at", mode="before")
    @classmethod
    def parse_date(cls, v: str):
        if isinstance(v, str):
            return utils.from_string_to_datetime(v)
        raise ValueError(f"{v} is not datetime string")
