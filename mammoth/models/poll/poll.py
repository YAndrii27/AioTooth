from pydantic import BaseModel
from datetime import datetime

from ..custom_emoji import CustomEmoji


class Poll(BaseModel):
    id: str
    expires_at: datetime | None
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: int | None
    options: list[str]
    emoji: CustomEmoji
    voted: bool | None
    own_votes: list[int] | None
