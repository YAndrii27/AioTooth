from pydantic import BaseModel

from ..field import Field
from ...enums.status_visibility import StatusVisibility


class Source(BaseModel):
    note: str | None = None
    fields: list[Field]
    privacy: StatusVisibility
    sensitive: bool
    language: str | None
    follow_requests_count: int
