from pydantic import BaseModel


class Domain(BaseModel):
    url: str
