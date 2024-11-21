from pydantic import BaseModel

from . import Account, Source
from ..role import Role


class CredentialAccount(Account, BaseModel):
    source: Source
    role: Role
