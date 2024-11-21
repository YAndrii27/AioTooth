from pydantic import BaseModel

from .acount import Account


class FamiliarFollowers(BaseModel):
    id: str
    accounts: list[Account]
