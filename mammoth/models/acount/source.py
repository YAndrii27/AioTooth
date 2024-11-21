from typing import Optional
from pydantic import BaseModel

from ..field import Field
from ...enums.status_visibility import StatusVisibility


class Source(BaseModel):
    note: Optional[str] = None
    fields: list[Field]
    privacy: StatusVisibility
    sensitive: bool
    language: Optional[str]
    follow_requests_count: int
