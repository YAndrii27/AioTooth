from typing import Optional
from pydantic import BaseModel


class CustomEmoji(BaseModel):
    shortcode: str
    url: str
    static_url: str
    visible_in_picker: bool
    category: Optional[str]
