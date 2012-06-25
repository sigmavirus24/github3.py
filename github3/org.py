"""
github3.org
===========

This module contains all of the classes related to organizations.

"""

from json import dumps
from .event import Event
from .models import BaseAccount, GitHubCore
from .repo import Repository
from .user import User


class Team(GitHubCore):
    def __init__(self, team, session):
        super(Team, self).__init__(session)
        self._update_(team)

    def __repr__(self):
        return '<Team [%s]>' % self._name

    def _update_(self, team):
        self._api = team.get('url')
        self._name = team.get('name')
        self._id = team.get('id')
        self._perm = team.get('permissions')
        self._members = team.get('members_count')
        self._repos = team.get('repos_count')

    def add_member(self, login):
        """Add ``login`` to this team.
        
        :returns: bool
        """
        url = '{0}/members/{1}'.format(self._api, login)
        return self._put(url)

    def add_repo(self, repo):
        """Add ``repo`` to this team.

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :returns: bool
        """
        url = '{0}/repos/{1}'.format(self._api, repo)
        return self._put(url)

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
        :param has_downloads: (optional), If ``True``, enable downloads for this
            repository. API default: ``True``
        :type has_downloads: bool
        :param team_id: (optional), id of the team that will be granted
            access to this repository
        :type team_id: int
        :returns: :class:`Repository <github3.repo.Repository>`
        """
        url = self._github_url + '/user/repos'
        data = dumps({'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads})
        if team_id > 0:
            data.update({'team_id': team_id})
        json = self._post(url, data)
        return Repository(json, self._session) if json else None

    def delete(self):
        """Delete this team.
        
        :returns: bool
        """
        return self._delete(self._api)

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
            json = self._patch(self._api, data)
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
        url = '{0}/repos/{1}'.format(self._api, repo)
        return self._session.get(url).status_code == 204

    @property
    def id(self):
        """Unique ID of the team."""
        return self._id

    def is_member(self, login):
        """Check if ``login`` is a member of this team.
        
        :param login: (required), login name of the user
        :type login: str
        :returns: bool
        """
        url = '{0}/members/{1}'.format(self._api, login)
        return self._session.get(url).status_code == 204

    def list_members(self):
        """List the members of this team.
        
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        url = self._api + '/members'
        resp = self._get(url)
        ses = self._session
        return [User(m, ses) for m in json]

    def list_repos(self):
        """List the repositories this team has access to.
        
        :returns: list of :class:`Repository <github3.repo.Repository>` objects
        """
        url = self._api + '/repos'
        resp = self._get(url)
        ses = self._session
        return [Repository(r, ses) for r in json]

    @property
    def members_count(self):
        """Number of members in this team."""
        return self._members

    @property
    def name(self):
        """This team's name."""
        return self._name

    def remove_member(self, login):
        """Remove ``login`` from this team.
        
        :param login: (required), login of the member to remove
        :type login: str
        :returns: bool
        """
        url = '{0}/members/{1}'.format(self._api, login)
        return self._delete(url)

    def remove_repo(self, repo):
        """Remove ``repo`` from this team.

        :param repo: (required), form: 'user/repo'
        :type repo: str
        :returns: bool
        """
        url = '{0}/repos/{1}'.format(self._api, repo)
        return self._delete(url)

    @property
    def repos_count(self):
        """Number of repos owned by this org."""
        return self._repos


class Organization(BaseAccount):
    """The :class:`Organization <Organization>` object."""
    def __init__(self, org, session):
        super(Organization, self).__init__(org, session)
        self._update_(org)
        if not self._type:
            self._type = 'Organization'

    def __repr__(self):
        return '<Organization [%s:%s]>' % (self._login, self._name)

    def _list_members(self, tail):
        """List members of this organization."""
        url = self._api + tail
        json = self._get(url)
        ses = self._session
        return [User(memb, ses) for memb in json]

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

    def conceal_member(self, login):
        """Conceal ``login``'s membership in this organization.
        
        :returns: bool
        """
        url = '{0}/public_members/{1}'.format(self._api, login)
        return self._delete(url)

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
        url = self._api + '/teams'
        json = self._post(url, data)
        return Team(json, self._session) if json else None

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
        json = self._patch(self._api,
                dumps({'billing_email': billing_email,
                    'company': company, 'email': email,
                    'location': location,  'name': name}))
        if json:
            self._update_(json)
            return True
        return False

    def is_member(self, login):
        """Check if the user with login ``login`` is a member.
        
        :returns: bool
        """
        url = '{0}/members/{1}'.format(self._api, login)
        return self._session.get(url).status_code == 204

    def is_public_member(self, login):
        """Check if the user with login ``login`` is a public member.
        
        :returns: bool
        """
        url = '{0}/public_members/{1}'.format(self._api, login)
        return self._session.get(url).status_code == 204

    def list_events(self):
        """List events for this org.

        :returns: list of :class:`Event <event.Event>`\ s
        """
        url = self._api + '/events'
        json = self._get(url)
        return [Event(e, self._session) for e in json]

    def list_members(self):
        """List members of this organization.
        
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        return self._list_members('/members')

    def list_public_members(self):
        """List public members of this organization.
        
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        return self._list_members('/public_members')

    def list_repos(self, type=''):
        """List repos for this organization.

        :param type: (optional), accepted values:
            ('all', 'public', 'member', 'private'), API default: 'all'
        :type type: str
        :returns: list of :class:`Repository <github3.repo.Repository>` objects
        """
        url = self._api + '/repos'
        if type in ('all', 'public', 'member', 'private'):
            url = '?'.join([url, 'type=' + type])
        json = self._get(url)
        ses = self._session
        return [Repository(r, ses) for r in json]

    def list_teams(self):
        """List teams that are part of this organization.
        
        :returns: list of :class:`Team <Team>`\ s
        """
        url = self._api + '/teams'
        json = self._get(url)
        ses = self._session
        return [Team(team, ses) for team in json]

    @property
    def private_repos(self):
        """Number of private repositories."""
        return self._private_repos

    def publicize_member(self, login):
        """Make ``login``'s membership in this organization public.
        
        :returns: bool
        """
        url = '{0}/public_members/{1}'.format(self._api, login)
        return self._put(url)

    def remove_member(self, login):
        """Remove the user with login ``login`` from this
        organization.
        
        :returns: bool
        """
        url = '{0}/members/{1}'.format(self._api, login)
        return self._delete(url)

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

    def team(self, team_id):
        """Returns Team object with information about team specified by
        ``team_id``.

        :param team_id: (required), unique id for the team
        :type team_id: int
        :returns: :class:`Team <Team>`
        """
        json = None
        if int(team_id) > 0:
            url = '{0}/teams/{1}'.format(self._github_url, str(team_id))
            json = self._get(url)
        return Team(json, self._session) if json else None
