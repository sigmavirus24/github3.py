# -*- coding: utf-8 -*-
"""
github3.orgs
============

This module contains all of the classes related to organizations.

"""
from __future__ import unicode_literals

from json import dumps
from github3.events import Event
from github3.models import BaseAccount, GitHubCore
from github3.repos import Repository
from github3.users import User
from github3.decorators import requires_auth
from uritemplate import URITemplate


class Team(GitHubCore):

    """The :class:`Team <Team>` object.

    Two team instances can be checked like so::

        t1 == t2
        t1 != t2

    And is equivalent to::

        t1.id == t2.id
        t1.id != t2.id

    See also: http://developer.github.com/v3/orgs/teams/

    """

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
        members = team.get('members_url')
        #: Members URL Template. Expands with ``member``
        self.members_urlt = URITemplate(members) if members else None
        #: Number of repos owned by this team.
        self.repos_count = team.get('repos_count')
        #: Repositories url (not a template)
        self.repositories_url = team.get('repositories_url')

    def _repr(self):
        return '<Team [{0}]>'.format(self.name)

    def _update_(self, team):
        self.__init__(team, self._session)

    @requires_auth
    def add_member(self, username):
        """Add ``username`` to this team.

        :param str username: the username of the user you would like to add to
            the team.
        :returns: bool
        """
        url = self._build_url('members', username, base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def add_repository(self, repository):
        """Add ``repository`` to this team.

        :param str repository: (required), form: 'user/repo'
        :returns: bool
        """
        url = self._build_url('repos', repository, base_url=self._api)
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

        :param str name: (required)
        :param str permission: (optional), ('pull', 'push', 'admin')
        :returns: bool
        """
        if name:
            data = {'name': name, 'permission': permission}
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
            if json:
                self._update_(json)
                return True
        return False

    def has_repo(self, repo):
        """Checks if this team has access to ``repo``

        :param str repo: (required), form: 'user/repo'
        :returns: bool
        """
        url = self._build_url('repos', repo, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def is_member(self, login):
        """Check if ``login`` is a member of this team.

        :param str login: (required), login name of the user
        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def members(self, number=-1, etag=None):
        """Iterate over the members of this team.

        :param int number: (optional), number of users to iterate over.
            Default: -1 iterates over all values
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def repositories(self, number=-1, etag=None):
        """Iterate over the repositories this team has access to.

        :param int number: (optional), number of repos to iterate over.
            Default: -1 iterates over all values
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
            objects
        """
        url = self._build_url('repos', base_url=self._api)
        return self._iter(int(number), url, Repository, etag=etag)

    @requires_auth
    def remove_member(self, username):
        """Remove ``username`` from this team.

        :param str username: (required), username of the member to remove
        :returns: bool
        """
        url = self._build_url('members', username, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def remove_repository(self, repository):
        """Remove ``repository`` from this team.

        :param str repository: (required), form: 'user/repo'
        :returns: bool
        """
        url = self._build_url('repos', repository, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)


class Organization(BaseAccount):

    """The :class:`Organization <Organization>` object.

    Two organization instances can be checked like so::

        o1 == o2
        o1 != o2

    And is equivalent to::

        o1.id == o2.id
        o1.id != o2.id

    See also: http://developer.github.com/v3/orgs/

    """

    def __init__(self, org, session=None):
        super(Organization, self).__init__(org, session)
        self.type = self.type or 'Organization'

        #: Events url (not a template)
        self.events_url = org.get('events_url')
        #: Number of private repositories.
        self.private_repos = org.get('private_repos', 0)

        members = org.get('members_url')
        #: Members URL Template. Expands with ``member``
        self.members_urlt = URITemplate(members) if members else None

        members = org.get('public_members_url')
        #: Public Members URL Template. Expands with ``member``
        self.public_members_urlt = URITemplate(members) if members else None
        #: Repositories url (not a template)
        self.repos_url = org.get('repos_url')

    @requires_auth
    def add_member(self, login, team_id):
        """Add ``login`` to ``team`` and thereby to this organization.

        Any user that is to be added to an organization, must be added
        to a team as per the GitHub api.

        .. versionchanged:: 1.0

            The second parameter used to be ``team`` but has been changed to
            ``team_id``. This parameter is now required to be an integer to
            improve performance of this method.

        :param str login: (required), login name of the user to be added
        :param int team_id: (required), team id
        :returns: bool
        """
        if int(team_id) < 0:
            return False

        url = self._build_url('teams', str(team_id), 'members', str(login))
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def add_repository(self, repository, team_id):
        """Add ``repository`` to ``team``.

        .. versionchanged:: 1.0

            The second parameter used to be ``team`` but has been changed to
            ``team_id``. This parameter is now required to be an integer to
            improve performance of this method.

        :param str repository: (required), form: 'user/repo'
        :param int team_id: (required), team id
        :returns: bool
        """
        if int(team_id) < 0:
            return False

        url = self._build_url('teams', str(team_id), 'repos', str(repository))
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def create_repository(self, name, description='', homepage='',
                          private=False, has_issues=True, has_wiki=True,
                          team_id=0, auto_init=False, gitignore_template='',
                          license_template=''):
        """Create a repository for this organization.

        If the client is authenticated and a member of the organization, this
        will create a new repository in the organization.

        :param str name: (required), name of the repository
        :param str description: (optional)
        :param str homepage: (optional)
        :param bool private: (optional), If ``True``, create a private
            repository. API default: ``False``
        :param bool has_issues: (optional), If ``True``, enable issues for
            this repository. API default: ``True``
        :param bool has_wiki: (optional), If ``True``, enable the wiki for
            this repository. API default: ``True``
        :param int team_id: (optional), id of the team that will be granted
            access to this repository
        :param bool auto_init: (optional), auto initialize the repository.
        :param str gitignore_template: (optional), name of the template; this
            is ignored if auto_int = False.
        :param str license_template: (optional), name of the license; this
            is ignored if auto_int = False.
        :returns: :class:`Repository <github3.repos.Repository>`

        .. warning: ``name`` should be no longer than 100 characters
        """
        url = self._build_url('repos', base_url=self._api)
        data = {'name': name, 'description': description,
                'homepage': homepage, 'private': private,
                'has_issues': has_issues, 'has_wiki': has_wiki,
                'license_template': license_template, 'auto_init': auto_init,
                'gitignore_template': gitignore_template}
        if int(team_id) > 0:
            data.update({'team_id': team_id})
        json = self._json(self._post(url, data), 201)
        return Repository(json, self) if json else None

    @requires_auth
    def conceal_member(self, username):
        """Conceal ``username``'s membership in this organization.

        :param str username: username of the organization member to conceal
        :returns: bool
        """
        url = self._build_url('public_members', username, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def create_team(self, name, repo_names=[], permission=''):
        """Create a new team and return it.

        This only works if the authenticated user owns this organization.

        :param str name: (required), name to be given to the team
        :param list repo_names: (optional) repositories, e.g.
            ['github/dotfiles']
        :param str permission: (optional), options:

            - ``pull`` -- (default) members can not push or administer
                repositories accessible by this team
            - ``push`` -- members can push and pull but not administer
                repositories accessible by this team
            - ``admin`` -- members can push, pull and administer
                repositories accessible by this team

        :returns: :class:`Team <Team>`
        """
        data = {'name': name, 'repo_names': repo_names,
                'permission': permission}
        url = self._build_url('teams', base_url=self._api)
        json = self._json(self._post(url, data), 201)
        return Team(json, self._session) if json else None

    @requires_auth
    def edit(self, billing_email=None, company=None, email=None, location=None,
             name=None):
        """Edit this organization.

        :param str billing_email: (optional) Billing email address (private)
        :param str company: (optional)
        :param str email: (optional) Public email address
        :param str location: (optional)
        :param str name: (optional)
        :returns: bool
        """
        json = None
        data = {'billing_email': billing_email, 'company': company,
                'email': email, 'location': location, 'name': name}
        self._remove_none(data)

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

    def events(self, number=-1, etag=None):
        """Iterate over events for this org.

        :param int number: (optional), number of events to return. Default: -1
            iterates over all events available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def members(self, number=-1, etag=None):
        """Iterate over members of this organization.

        :param int number: (optional), number of members to return. Default:
            -1 will return all available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def public_members(self, number=-1, etag=None):
        """Iterate over public members of this organization.

        :param int number: (optional), number of members to return. Default:
            -1 will return all available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('public_members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def repositories(self, type='', number=-1, etag=None):
        """Iterate over repos for this organization.

        :param str type: (optional), accepted values:
            ('all', 'public', 'member', 'private', 'forks', 'sources'), API
            default: 'all'
        :param int number: (optional), number of members to return. Default:
            -1 will return all available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        url = self._build_url('repos', base_url=self._api)
        params = {}
        if type in ('all', 'public', 'member', 'private', 'forks', 'sources'):
            params['type'] = type
        return self._iter(int(number), url, Repository, params, etag)

    @requires_auth
    def teams(self, number=-1, etag=None):
        """Iterate over teams that are part of this organization.

        :param int number: (optional), number of teams to return. Default: -1
            returns all available teams.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Team <Team>`\ s
        """
        url = self._build_url('teams', base_url=self._api)
        return self._iter(int(number), url, Team, etag=etag)

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

        :param str repo: (required), form: 'user/repo'
        :param str team: (required)
        :returns: bool
        """
        for t in self.teams():
            if team == t.name:
                return t.remove_repo(repo)
        return False

    @requires_auth
    def team(self, team_id):
        """Returns Team object with information about team specified by
        ``team_id``.

        :param int team_id: (required), unique id for the team
        :returns: :class:`Team <Team>`
        """
        json = None
        if int(team_id) > 0:
            url = self._build_url('teams', str(team_id))
            json = self._json(self._get(url), 200)
        return Team(json, self._session) if json else None
