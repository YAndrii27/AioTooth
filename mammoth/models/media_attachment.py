from typing import Any
from pydantic import BaseModel


class MediaAttachment(BaseModel):
    id: str
    media_type: str
    url: str
    preview_url: str | None
    remote_url: str | None
    meta: dict[Any, Any]  # TODO: find out more about Paperclip's metadata
    description: str | None
    blurhash: str | None
    text_url: str | None
