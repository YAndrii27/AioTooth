from pydantic import BaseModel


class StatusTag(BaseModel):
    name: str
    url: str
