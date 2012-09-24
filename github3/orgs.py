"""
github3.orgs
============

This module contains all of the classes related to organizations.

"""

from json import dumps
from github3.events import Event
from github3.models import BaseAccount, GitHubCore
from github3.repos import Repository
from github3.users import User
from github3.decorators import requires_auth


class Team(GitHubCore):
    def __init__(self, team, session=None):
        super(Team, self).__init__(team, session)
        self._api = team.get('url', '')
        #: This team's name.
        self.name = team.get('name')
        #: Unique ID of the team.
        self.id = team.get('id')
        #: Permission leve of the group
        self.permission = team.get('permission')
        #: Number of members in this team.
        self.members_count = team.get('members_count')
        #: Number of repos owned by this team.
        self.repos_count = team.get('repos_count')

    def __repr__(self):
        return '<Team [{0}]>'.format(self.name)

    def _update_(self, team):
        self.__init__(team, self._session)

    @requires_auth
    def add_member(self, login):
        """Add ``login`` to this team.

        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def add_repo(self, repo):
        """Add ``repo`` to this team.

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :returns: bool
        """
        url = self._build_url('repos', repo, base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def delete(self):
        """Delete this team.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, name, permission=''):
        """Edit this team.

        :param name: (required)
        :type name: str
        :param permission: (optional), ('pull', 'push', 'admin')
        :type permission: str
        :returns: bool
        """
        if name:
            data = dumps({'name': name, 'permission': permission})
            json = self._json(self._patch(self._api, data=data), 200)
            if json:
                self._update_(json)
                return True
        return False

    def has_repo(self, repo):
        """Checks if this team has access to ``repo``

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :returns: bool
        """
        url = self._build_url('repos', repo, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def is_member(self, login):
        """Check if ``login`` is a member of this team.

        :param login: (required), login name of the user
        :type login: str
        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def list_members(self):
        """List the members of this team.

        :returns: list of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('members', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [User(m, self) for m in json]

    def list_repos(self):
        """List the repositories this team has access to.

        :returns: list of :class:`Repository <github3.repos.Repository>`
            objects
        """
        url = self._build_url('repos', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Repository(r, self) for r in json]

    @requires_auth
    def remove_member(self, login):
        """Remove ``login`` from this team.

        :param login: (required), login of the member to remove
        :type login: str
        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def remove_repo(self, repo):
        """Remove ``repo`` from this team.

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :returns: bool
        """
        url = self._build_url('repos', repo, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)


class Organization(BaseAccount):
    """The :class:`Organization <Organization>` object."""
    def __init__(self, org, session=None):
        super(Organization, self).__init__(org, session)
        if not self.type:
            self.type = 'Organization'

        #: Number of private repositories.
        self.private_repos = org.get('private_repos', 0)

    def __repr__(self):
        return '<Organization [{0}:{1}]>'.format(self.login, self.name)

    def _list_members(self, tail):
        """List members of this organization."""
        url = self._api + tail
        json = self._json(self._get(url), 200)
        return [User(memb, self) for memb in json]

    @requires_auth
    def add_member(self, login, team):
        """Add ``login`` to ``team`` and thereby to this organization.

        Any user that is to be added to an organization, must be added
        to a team as per the GitHub api.

        :param login: (required), login name of the user to be added
        :type login: str
        :param team: (required), team name
        :type team: str
        :returns: bool
        """
        teams = self.list_teams()
        for t in teams:
            if team == t.name:
                return t.add_member(login)
        return False

    @requires_auth
    def add_repo(self, repo, team):
        """Add ``repo`` to ``team``.

        :param repo: (required), string, form: 'user/repo'
        :param team: (required), string
        """
        teams = self.list_teams()
        for t in teams:
            if team == t.name:
                return t.add_repo(repo)
        return False

    @requires_auth
    def create_repo(self,
        name,
        description='',
        homepage='',
        private=False,
        has_issues=True,
        has_wiki=True,
        has_downloads=True,
        team_id=0):
        """Create a repository for this organization if the authenticated user
        is a member.

        :param name: (required), name of the repository
        :type name: str
        :param description: (optional)
        :type description: str
        :param homepage: (optional)
        :type homepage: str
        :param private: (optional), If ``True``, create a private repository.
            API default: ``False``
        :type private: bool
        :param has_issues: (optional), If ``True``, enable issues for this
            repository. API default: ``True``
        :type has_issues: bool
        :param has_wiki: (optional), If ``True``, enable the wiki for this
            repository. API default: ``True``
        :type has_wiki: bool
        :param has_downloads: (optional), If ``True``, enable downloads for
            this repository. API default: ``True``
        :type has_downloads: bool
        :param team_id: (optional), id of the team that will be granted
            access to this repository
        :type team_id: int
        :returns: :class:`Repository <github3.repos.Repository>`
        """
        url = self._build_url('repos', base_url=self._api)
        data = {'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads}
        if team_id > 0:
            data.update({'team_id': team_id})
        json = self._json(self._post(url, dumps(data)), 201)
        return Repository(json, self) if json else None

    @requires_auth
    def conceal_member(self, login):
        """Conceal ``login``'s membership in this organization.

        :returns: bool
        """
        url = self._build_url('public_members', login, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def create_team(self, name, repo_names=[], permissions=''):
        """Assuming the authenticated user owns this organization,
        create and return a new team.

        :param name: (required), name to be given to the team
        :type name: str
        :param repo_names: (optional) repositories, e.g.
            ['github/dotfiles']
        :type repo_names: list
        :param permissions: (optional), options:

            - ``pull`` -- (default) members can not push or administer
                repositories accessible by this team
            - ``push`` -- members can push and pull but not administer
                repositories accessible by this team
            - ``admin`` -- members can push, pull and administer
                repositories accessible by this team

        :type permissions: str
        :returns: :class:`Team <Team>`
        """
        data = dumps({'name': name, 'repo_names': repo_names,
            'permissions': permissions})
        url = self._build_url('teams', base_url=self._api)
        json = self._json(self._post(url, data), 201)
        return Team(json, self._session) if json else None

    @requires_auth
    def edit(self,
        billing_email=None,
        company=None,
        email=None,
        location=None,
        name=None):
        """Edit this organization.

        :param billing_email: (optional) Billing email address (private)
        :type billing_email: str
        :param company: (optional)
        :type company: str
        :param email: (optional) Public email address
        :type email: str
        :param location: (optional)
        :type location: str
        :param name: (optional)
        :type name: str
        :returns: bool
        """
        json = None
        data = {'billing_email': billing_email, 'company': company,
            'email': email, 'location': location, 'name': name}
        for (k, v) in data.items():
            if v is None:
                del data[k]

        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)

        if json:
            self._update_(json)
            return True
        return False

    def is_member(self, login):
        """Check if the user with login ``login`` is a member.

        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def is_public_member(self, login):
        """Check if the user with login ``login`` is a public member.

        :returns: bool
        """
        url = self._build_url('public_members', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def list_events(self):
        """List events for this org.

        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Event(e, self._session) for e in json]

    def list_members(self):
        """List members of this organization.

        :returns: list of :class:`User <github3.users.User>`\ s
        """
        return self._list_members('/members')

    def list_public_members(self):
        """List public members of this organization.

        :returns: list of :class:`User <github3.users.User>`\ s
        """
        return self._list_members('/public_members')

    def list_repos(self, type=''):
        """List repos for this organization.

        :param type: (optional), accepted values:
            ('all', 'public', 'member', 'private'), API default: 'all'
        :type type: str
        :returns: list of :class:`Repository <github3.repos.Repository>`
            objects
        """
        url = self._build_url('repos', base_url=self._api)
        params = {}
        if type in ('all', 'public', 'member', 'private'):
            params['type'] = type
        json = self._json(self._get(url, params=params), 200)
        return [Repository(r, self) for r in json]

    @requires_auth
    def list_teams(self):
        """List teams that are part of this organization.

        :returns: list of :class:`Team <Team>`\ s
        """
        url = self._build_url('teams', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Team(team, self) for team in json]

    @requires_auth
    def publicize_member(self, login):
        """Make ``login``'s membership in this organization public.

        :returns: bool
        """
        url = self._build_url('public_members', login, base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def remove_member(self, login):
        """Remove the user with login ``login`` from this
        organization.

        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def remove_repo(self, repo, team):
        """Remove ``repo`` from ``team``.

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :param team: (required)
        :type team: str
        :returns: bool
        """
        teams = self.list_teams()
        for t in teams:
            if team == t.name:
                return t.remove_repo(repo)
        return False

    @requires_auth
    def team(self, team_id):
        """Returns Team object with information about team specified by
        ``team_id``.

        :param team_id: (required), unique id for the team
        :type team_id: int
        :returns: :class:`Team <Team>`
        """
        json = None
        if int(team_id) > 0:
            url = self._build_url('teams', str(team_id))
            json = self._json(self._get(url), 200)
        return Team(json, self._session) if json else None
