from pydantic import BaseModel

from ...enums.preview_type import PreviewType
from ..preview.preview_author import PreviewAuthor


class PreviewCard(BaseModel):
    url: str
    title: str
    description: str
    preview_type: PreviewType
    authors: list[PreviewAuthor]
    author_name: str
    author_url: str
    provider_name: str
    html: str
    width: int
    height: int
    image: str | None
    embed_url: str
    blurhash: str | None
