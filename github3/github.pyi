"""This module contains the type stubs for github3.github."""
from typing import Dict, List, Union, Optional

from . import auths
from . import events
from .gists import gist
from .issues import issue
from . import orgs
from .repos import repo
from . import structs
from . import users

AuthorizationsIterator = structs.GitHubIterator[auths.Authorization]
EventsIterator = structs.GitHubIterator[events.Event]
OrganizationsIterator = structs.GitHubIterator[orgs.ShortOrganization]
RepositoriesIterator = structs.GitHubIterator[repo.ShortRepository]
UsersIterator = structs.GitHubIterator[users.ShortUser]


class GitHub:
    def __init__(
        self,
        username: str='',
        password: str='',
        token: str='',
    ) -> None:
        ...

    def add_email_addresses(
        self,
        addresses: List[str]=[],
    ) -> List[users.Email]:
        ...

    def all_events(
        self,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> EventsIterator:
        ...

    def all_organizations(
        self,
        number: int=-1,
        since: Optional[int]=None,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
    ) -> OrganizationsIterator:
        ...

    def all_repositories(
        self,
        number: int=-1,
        since: Optional[int]=None,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
    ) -> RepositoriesIterator:
        ...

    def all_users(
        self,
        number: int=-1,
        etag: Optional[str]=None,
        per_page: Optional[int]=None,
        since: Optional[int]=None,
    ) -> UsersIterator:
        ...

    def authorization(
        self,
        id_num: Union[int, str],
    ) -> AuthorizationsIterator:
        ...

    def authorizations(
        self,
        number: int=-1,
        etag: Optional[str]=None,
    ) -> AuthorizationsIterator:
        ...

    def authorize(
        self,
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
        self,
        access_token: str,
    ) -> bool:
        ...

    def create_gist(
        self,
        description: str,
        files: Dict[str, Dict[str, str]],
        public: bool=True,
    ) -> gist.Gist:
        ...

    def create_issue(
        self,
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
