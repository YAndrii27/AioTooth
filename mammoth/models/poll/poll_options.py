from typing import Optional
from pydantic import BaseModel


class PollOption(BaseModel):
    title: str
    votes_count: Optional[int]
