from typing import Optional
from pydantic import BaseModel


class PollOption(BaseModel):
    title: str


class Poll(BaseModel):
    id: str
    translation: list[PollOption]


class Attachment(BaseModel):
    id: str
    description: str


class Translation(BaseModel):
    content: str
    spoiler_text: str
    poll: Optional[Poll]
    media_attachments: Optional[Attachment]
    detected_source_language: str
    provider: str
