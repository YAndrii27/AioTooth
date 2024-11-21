from pydantic import BaseModel


class StatusMentions(BaseModel):
    id: str
    username: str
    url: str
    acct: str
