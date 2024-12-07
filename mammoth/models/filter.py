from typing import Optional
from pydantic import BaseModel

from ..enums import Context, FilterAction
from .filter_keywords import FilterKeyword
from .filter_status import FilterStatus


class Filter(BaseModel):
    id: str
    title: str
    context: Context
    expires_at: Optional[str]
    filter_action: FilterAction
    keywords: FilterKeyword
    statuses: FilterStatus
