from pydantic import BaseModel

from ..enums import RepliesPolicy


class AccountsList(BaseModel):
    id: str
    title: str
    replies_policy: RepliesPolicy
