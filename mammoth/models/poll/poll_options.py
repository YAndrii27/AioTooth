from pydantic import BaseModel


class PollOption(BaseModel):
    title: str
    votes_count: int | None
