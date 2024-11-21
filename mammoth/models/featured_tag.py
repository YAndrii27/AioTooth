from pydantic import BaseModel, field_validator

from .. import utils


class FeaturedTag(BaseModel):
    id: str
    name: str
    url: str
    statuses_count: int
    last_status_at: str

    @field_validator("last_status_at", mode="before")
    @classmethod
    def parse_date(cls, v: str):
        if isinstance(v, str):
            return utils.from_string_to_datetime(v)
        raise ValueError(f"{v} is not datetime string")
