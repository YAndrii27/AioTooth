from pydantic import BaseModel

from .account import Account
from .source import Source


# Yes, thanks Mastodon
class AccountWithSource(Account, BaseModel):
    source: Source
