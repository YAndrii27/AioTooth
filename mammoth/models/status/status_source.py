from pydantic import BaseModel


class StatusSource(BaseModel):
    id: str
    text: str
    spoiler_text: str
