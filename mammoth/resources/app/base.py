from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...app import MastodonApp


class BaseAppResource:
    def __init__(self, app: "MastodonApp") -> None:
        self.app = app
