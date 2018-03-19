"""This module contains the type stubs for github3.github."""
from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

from . import auths
from . import decorators
from . import events
from . import models
from . import orgs
from . import structs
from . import users
from .gists import gist
from .issues import issue
from .repos import repo

T = TypeVar('T', bound='GitHub')


class GitHub(models.GitHubCore):
    def __init__(
        self: T,
        username: str='',
        password: str='',
        token: str='',
    ) -> None:
        ...

    @decorators.requires_auth
    def add_email_addresses(
        self: T,
        addresses: List[str]=[],
    ) -> List[users.Email]:
        ...

    def all_events(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[events.Event]:
        ...

    def all_organizations(
        self: T,
        number: int=-1,
        since: Optional[int]=None,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
    ) -> structs.GitHubIterator[orgs.ShortOrganization]:
        ...

    def all_repositories(
        self: T,
        number: int=-1,
        since: Optional[int]=None,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
    ) -> structs.GitHubIterator[repo.ShortRepository]:
        ...

    def all_users(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
        since: Optional[int]=None,
    ) -> structs.GitHubIterator[users.ShortUser]:
        ...

    @decorators.requires_basic_auth
    def authorization(
        self: T,
        id_num: Union[int, str],
    ) -> auths.Authorization:
        ...

    def authorizations(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[auths.Authorization]:
        ...

    def authorize(
        self: T,
        username: str,
        password: str,
        scopes: Optional[List[str]]=None,
        note: str='',
        note_url: str='',
        client_id: str='',
        client_secret: str='',
    ) -> auths.Authorization:
        ...

    def check_authorization(
        self: T,
        access_token: str,
    ) -> bool:
        ...

    def create_gist(
        self: T,
        description: str,
        files: Dict[str, Dict[str, str]],
        public: bool=True,
    ) -> gist.Gist:
        ...

    @decorators.requires_auth
    def create_issue(
        self: T,
        owner: str,
        repository: str,
        title: str,
        body: Optional[str]=None,
        assignee: Optional[str]=None,
        milestone: Optional[int]=None,
        labels: List[str]=[],
        assignees: Optional[List[str]]=None,
    ) -> issue.ShortIssue:
        ...

    @decorators.requires_auth
    def create_key(
        self: T,
        title: str,
        key: str,
        read_only: bool=False,
    ) -> users.Key:
        ...

    @decorators.requires_auth
    def create_repository(
        self: T,
        name: str,
        description: str='',
        homepage: str='',
        private: bool=False,
        has_issues: bool=True,
        has_wiki: bool=True,
        auto_init: bool=False,
        gitignore_template: str='',
    ) -> repo.Repository:
        ...

    @decorators.requires_auth
    def delete_email_addresses(
        self: T,
        addresses: List[str],
    ) -> bool:
        ...

    @decorators.requires_auth
    def emails(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[users.Email]:
        ...

    def emojis(self: T) -> Dict[str, str]:
        ...

    def feeds(self: T) -> Dict[str, Any]:
        ...

    @decorators.requires_auth
    def follow(
        self: T,
        username: str
    ) -> bool:
        ...

    def followed_by(
        self: T,
        username: str,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[users.ShortUser]:
        ...

    @decorators.requires_auth
    def followers(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[users.ShortUser]:
        ...

    def followers_of(
        self: T,
        username: str,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[users.ShortUser]:
        ...

    @decorators.requires_auth
    def following(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[users.ShortUser]:
        ...

    def gist(
        self: T,
        id_num: int,
    ) -> gist.Gist:
        ...

    @decorators.requires_auth
    def gists(
        self: T,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[gist.ShortGist]:
        ...

    def gists_by(
        self: T,
        username: str,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> structs.GitHubIterator[gist.ShortGist]:
        ...
