from pydantic import BaseModel


class CustomEmoji(BaseModel):
    shortcode: str
    url: str
    static_url: str
    visible_in_picker: bool
    category: str | None
