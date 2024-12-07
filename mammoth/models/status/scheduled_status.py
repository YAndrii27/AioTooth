from typing import Optional
from pydantic import BaseModel

from ..media_attachment import MediaAttachment
from ..poll import NewPoll


class ScheduledStatusParams(BaseModel):
    text: str
    poll: Optional[NewPoll]
    media_ids: Optional[list[str]]
    sensitive: Optional[bool]
    spoiler_text: Optional[str]
    visibility: str
    in_reply_to_id: Optional[int]
    language: Optional[str]
    application_id: int
    scheduled_at: None
    idempotency: Optional[str]
    with_rate_limit: bool


class ScheduledStatus(BaseModel):
    id: int
    scheduled_at: str
    params: ScheduledStatusParams
    media_attachments: list[MediaAttachment]
