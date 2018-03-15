from typing import (
    Any,
    Dict,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
)

from . import session


Subclass = TypeVar('Subclass', bound='GitHubCore')
Core = TypeVar('Core', bound='GitHubCore')
Sessionish = Union[session.GitHubSession, GitHubCore]
FullClass = TypeVar('FullClass')

class GitHubCore(Generic[FullClass]):
    _refresh_to = None # type: Optional[FullClass]

    def __init__(
        self: Core,
        json: Dict[str, Any],
        session: Sessionish,
    ) -> None:
        ...

    def as_dict(self: Core) -> Dict[str, Any]:
        ...

    def as_json(self: Core) -> str:
        ...

    @classmethod
    def from_dict(
        cls: Type[Subclass],
        json_dict: Dict[str, Any],
        session: Sessionish,
    ) -> Subclass:
        ...

    @classmethod
    def from_json(
        cls: Type[Subclass],
        json_dict: str,
        session: Sessionish,
    ) -> Subclass:
        ...

    @property
    def ratelimit_remaining(self: Core) -> int:
        ...

    def refresh(
        self: Core,
        conditional: bool,
    ) -> Union[Core, FullClass]:
        ...

    def new_session(self: Core) -> session.GitHubSession:
        ...
