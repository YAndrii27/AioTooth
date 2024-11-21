from typing import Optional
from pydantic import BaseModel

from ..acount import Account


class PreviewAuthor(BaseModel):
    name: str
    url: str
    account: Optional[Account]
