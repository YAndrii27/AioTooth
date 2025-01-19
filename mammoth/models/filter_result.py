from pydantic import BaseModel

from .filter import Filter


class FilterResult(BaseModel):
    filter: Filter
    keyword_matches: list[str] | None
    status_matches: list[str] | None
