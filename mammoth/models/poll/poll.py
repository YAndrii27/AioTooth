from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from ..custom_emoji import CustomEmoji


class Poll(BaseModel):
    id: str
    expires_at: Optional[datetime]
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: Optional[int]
    options: list[str]
    emoji: CustomEmoji
    voted: Optional[bool]
    own_votes: Optional[list[int]]
