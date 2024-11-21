from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MastodonClient


class BaseAPI:
    def __init__(self, client: "MastodonClient") -> None:
        self.client = client
