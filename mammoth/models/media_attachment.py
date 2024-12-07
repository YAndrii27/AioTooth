from typing import Optional, Any
from pydantic import BaseModel


class MediaAttachment(BaseModel):
    id: str
    media_type: str
    url: str
    preview_url: Optional[str]
    remote_url: Optional[str]
    meta: dict[Any, Any]  # TODO: find out more about Paperclip's metadata
    description: Optional[str]
    blurhash: Optional[str]
    text_url: Optional[str]
