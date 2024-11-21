from typing import Optional
from pydantic import BaseModel


class Field(BaseModel):
    name: str
    value: str
    verified_at: Optional[str]
