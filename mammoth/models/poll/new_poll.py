from pydantic import BaseModel


class NewPoll(BaseModel):
    """This class is describing poll object used during status creation"""
    options: list[str]
    expires_in: str
    multiple: bool
    hide_totals: bool
