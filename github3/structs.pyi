"""Stubs for github3.structs module."""
from typing import Dict, Iterator, TypeVar, Iterable, Generic, Optional

import requests

from . import session

ReturnClass = TypeVar('ReturnClass')

class GitHubIterator(Generic[ReturnClass], Iterable):
    original = ...  # type: int
    count = ...  # type: int
    url = ...  # type: str
    last_url = ...  # type: Optional[str]
    cls = ...  # type: ReturnClass
    params = ...  # type: Dict[str, str]
    etag = ...  # type: str
    headers = ...  # type: Dict[str, str]
    last_response = ...  # type: requests.models.Response
    last_status = ...  # type: int
    path = ...  # type: str

    def __init__(self, count: int, url: str, cls: ReturnClass,
                 session: session.GitHubSession, params: Dict[str, str],
                 etag: str, headers: Dict[str, str]) -> None:
        ...

    def __iter__(self) -> Iterator[ReturnClass]:
        ...

    def refresh(self, conditional: bool) -> GitHubIterator[ReturnClass]:
        ...
