from typing import Optional, Any
from pydantic import BaseModel

from ..acount import Account
from ..media_attachment import MediaAttachment
from ..custom_emoji import CustomEmoji


class StatusEdit(BaseModel):
    content: str
    spoiler_text: str
    sensitive: str
    created_at: str
    account: Account
    poll: Optional[dict[str, Any]]  # TODO: make better typing
    media_attachments: list[MediaAttachment]
    emoji: list[CustomEmoji]
