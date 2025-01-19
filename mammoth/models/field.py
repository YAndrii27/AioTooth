from pydantic import BaseModel


class Field(BaseModel):
    name: str
    value: str
    verified_at: str | None
