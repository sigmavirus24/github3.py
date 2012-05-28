"""
github3.org
===========

This module contains all of the classes related to organizations.

"""

from json import dumps
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
        self._api_url = team.get('url')
        self._name = team.get('name')
        self._id = team.get('id')
        self._perm = team.get('permissions')
        self._members = team.get('members_count')
        self._repos = team.get('repos_count')

    def add_member(self, login):
        """Add ``login`` to this team."""
        url = '/'.join([self._api_url, 'members', login])
        resp = self._put(url)
        if resp.status_code == 204:
            return True
        return False

    def add_repo(self, repo):
        """Add ``repo`` to this team.

        :param repo: (required), string, form: 'user/repo'
        """
        url = '/'.join([self._api_url, 'repos', repo])
        resp = self._put(url)
        if resp.status_code == 204:
            return True
        return False

    def edit(self, name, permission=''):
        """Edit this team.

        :param name: (required), string
        :param permission: (optional), ('pull', 'push', 'admin')
        """
        if name:
            data = dumps({'name': name, 'permission': permission})
            resp = self._patch(self._api_url, data)
            if resp.status_code == 200:
                self._update_(resp.json)
                return True
        return False

    def delete(self):
        """Delete this team."""
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    def has_repo(self, repo):
        """Checks if this team has access to ``repo``

        :param repo: (required), string, form: 'user/repo'
        """
        url = '/'.join([self._api_url, 'repos', repo])
        resp = self._get(url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def id(self):
        return self._id

    def is_member(self, login):
        """Check if ``login`` is a member of this team."""
        url = '/'.join([self._api_url, 'members', login])
        resp = self._get(url)
        if resp.status_code == 204:
            return True
        return False

    def list_members(self):
        """List the members of this team."""
        url = '/'.join([self._api_url, 'members'])
        resp = self._get(url)
        members = []
        if resp.status_code == 200:
            for member in resp.json:
                members.append(User(member, self._session))
        return members

    def list_repos(self):
        """List the repositories this team has access to."""
        url = '/'.join([self._api_url, 'repos'])
        resp = self._get(url)
        repos = []
        if resp.status_code == 200:
            for repo in resp.json:
                repos.append(Repository(repo, self._session))
        return repos

    @property
    def members_count(self):
        return self._members

    @property
    def name(self):
        return self._name

    def remove_member(self, login):
        """Remove ``login`` from this team."""
        url = '/'.join([self._api_url, 'members', login])
        resp = self._delete(url)
        if resp.status_code == 204:
            return True
        return False

    def remove_repo(self, repo):
        """Remove ``repo`` from this team.

        :param repo: (required), string, form: 'user/repo'
        """
        url = '/'.join([self._api_url, 'repos', repo])
        resp = self._delete(url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def repos_count(self):
        return self._repos


class Organization(BaseAccount):
    def __init__(self, org, session):
        super(Organization, self).__init__(org, session)
        self._update_(org)
        if not self._type:
            self._type = 'Organization'

    def __repr__(self):
        return '<Organization [%s:%s]>' % (self._login, self._name)

    def add_member(self, login, team):
        """Add ``login`` to ``team`` and thereby to this organization.

        Any user that is to be added to an organization, must be added
        to a team as per the GitHub api."""
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
        """Conceal ``login``'s membership in this organization."""
        url = '/'.join([self._api_url, 'public_members', login])
        resp = self._delete(url)
        if resp.status_code == 204:
            return True
        return False

    def create_team(self, name, repo_names=[], permissions=''):
        """Assuming the authenticated user owns this organization,
        create and return a new team.

        :param name: (required) string
        :param repo_names: (optional) list of repositories, e.g.
            ['github/dotfiles']
        :param permissions: (optional) string; options:
            ``pull`` - (default) members can not push or administer
            repositories accessible by this team
            ``push`` - members can push and pull but not administer
            repositories accessible by this team
            ``admin`` - members can push, pull and administer
            repositories accessible by this team
        """
        data = dumps({'name': name, 'repo_names': repo_names,
            'permissions': permissions})
        url = '/'.join([self._api_url, 'teams'])
        resp = self._post(url, data)
        if resp.status_code == 201:
            return Team(resp.json, self._session)
        return None

    def edit(self,
        billing_email=None,
        company=None,
        email=None,
        location=None,
        name=None):
        """Edit this organization.

        :param billing_email: (optional) Billing email address (private)
        :param company: (optional)
        :param email: (optional) Public email address
        :param location: (optional)
        :param name: (optional)
        """
        resp = self._patch(self._api_url,
                dumps({'billing_email': billing_email,
                    'company': company, 'email': email,
                    'location': location,  'name': name}))
        if resp.status_code == 200:
            self._update_(resp.json)
            return True
        return False

    def is_member(self, login):
        """Check if the user with login ``login`` is a member."""
        url = '/'.join([self._api_url, 'members', login])
        resp = self._get(url)
        if resp.status_code == 204:
            return True
        return False

    def is_public_member(self, login):
        """Check if the user with login ``login`` is a public member."""
        url = '/'.join([self._api_url, 'public_members', login])
        resp = self._get(url)
        if resp.status_code == 204:
            return True
        return False

    def list_members(self):
        """List members of this organization."""
        url = '/'.join([self._api_url, 'members'])
        members = []
        resp = self._get(url)
        if resp.status_code == 200:
            for member in resp.json:
                members.append(User(member, self._session))
        return members

    def list_public_members(self):
        """List public members of this organization."""
        url = '/'.join([self._api_url, 'public_members'])
        members = []
        resp = self._get(url)
        if resp.status_code == 200:
            for member in resp.json:
                members.append(User(member, self._session))
        return members

    def list_teams(self):
        """List teams that are part of this organization."""
        url = '/'.join([self._api_url, 'teams'])
        teams = []
        resp = self._get(url)
        if resp.status_code == 200:
            for team in resp.json:
                teams.append(Team(team, self._session))
        return teams

    @property
    def private_repos(self):
        return self._private_repos

    def publicize_member(self, login):
        """Make ``login``'s membership in this organization public."""
        url = '/'.join([self._api_url, 'public_members', login])
        resp = self._put(url)
        if resp.status_code == 204:
            return True
        return False

    def remove_member(self, login):
        """Remove the user with login ``login`` from this
        organization."""
        url = '/'.join([self._api_url, 'members', login])
        resp = self._delete(url)
        if resp.status_code == 204:
            return True
        return False

    def remove_repo(self, repo, team):
        """Remove ``repo`` from ``team``.

        :param repo: (required), string, form: 'user/repo'
        :param team: (required), string
        """
        teams = self.list_teams()
        for t in teams:
            if team == t.name:
                return t.remove_repo(repo)
        return False

    def team(self, team_id):
        """Returns Team object with information about team specified by
        ``team_id``.

        :param team_id: (required), int
        """
        team = None
        if int(team_id) > 0:
            url = '/'.join([self._github_url, 'teams', str(team_id)])
            resp = self._get(url)
            if resp.status_code == 200:
                team = Team(resp.json, self._session)
        return team
