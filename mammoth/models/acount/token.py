from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    scope: str
    created_at: int
