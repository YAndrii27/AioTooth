from pydantic import BaseModel

from ..media_attachment import MediaAttachment
from ..poll import NewPoll


class ScheduledStatusParams(BaseModel):
    text: str
    poll: NewPoll | None
    media_ids: list[str] | None
    sensitive: bool | None
    spoiler_text: str | None
    visibility: str
    in_reply_to_id: int | None
    language: str | None
    application_id: int
    scheduled_at: None
    idempotency: str | None
    with_rate_limit: bool


class ScheduledStatus(BaseModel):
    id: int
    scheduled_at: str
    params: ScheduledStatusParams
    media_attachments: list[MediaAttachment]
