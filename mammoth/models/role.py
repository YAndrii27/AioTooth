from pydantic import BaseModel


class Role(BaseModel):
    id: str
    name: str
    color: str
    permissions: str
    highlighted: bool
