# -*- coding: utf-8 -*-
"""
github3.orgs
============

This module contains all of the classes related to organizations.

"""
from __future__ import unicode_literals

import warnings

from json import dumps
from .events import Event
from .models import BaseAccount, GitHubCore
from .repos import Repository
from .users import User
from .decorators import requires_auth
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
    def add_member(self, login):
        """Add ``login`` to this team.

        :returns: bool
        """
        warnings.warn(
            'This is no longer supported by the GitHub API, see '
            'https://developer.github.com/changes/2014-09-23-one-more-week'
            '-before-the-add-team-member-api-breaking-change/',
            DeprecationWarning)
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def add_repo(self, repo):
        """Add ``repo`` to this team.

        :param str repo: (required), form: 'user/repo'
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

    @requires_auth
    def invite(self, username):
        """Invite the user to join this team.

        This returns a dictionary like so::

            {'state': 'pending', 'url': 'https://api.github.com/teams/...'}

        :param str username: (required), user to invite to join this team.
        :returns: dictionary
        """
        url = self._build_url('memberships', username, base_url=self._api)
        return self._json(self._put(url), 200)

    def is_member(self, login):
        """Check if ``login`` is a member of this team.

        :param str login: (required), login name of the user
        :returns: bool
        """
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def iter_members(self, number=-1, etag=None):
        """Iterate over the members of this team.

        :param int number: (optional), number of users to iterate over.
            Default: -1 iterates over all values
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def iter_repos(self, number=-1, etag=None):
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
    def membership_for(self, username):
        """Retrieve the membership information for the user.

        :param str username: (required), name of the user
        :returns: dictionary
        """
        url = self._build_url('memberships', username, base_url=self._api)
        json = self._json(self._get(url), 200)
        return json or {}

    @requires_auth
    def remove_member(self, login):
        """Remove ``login`` from this team.

        :param str login: (required), login of the member to remove
        :returns: bool
        """
        warnings.warn(
            'This is no longer supported by the GitHub API, see '
            'https://developer.github.com/changes/2014-09-23-one-more-week'
            '-before-the-add-team-member-api-breaking-change/',
            DeprecationWarning)
        url = self._build_url('members', login, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def revoke_membership(self, username):
        """Revoke this user's team membership.

        :param str username: (required), name of the team member
        :returns: bool
        """
        url = self._build_url('memberships', username, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def remove_repo(self, repo):
        """Remove ``repo`` from this team.

        :param str repo: (required), form: 'user/repo'
        :returns: bool
        """
        url = self._build_url('repos', repo, base_url=self._api)
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
        if not self.type:
            self.type = 'Organization'

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
    def add_member(self, login, team):
        """Add ``login`` to ``team`` and thereby to this organization.

        .. warning::
            This method is no longer valid. To add a member to a team, you
            must now retrieve the team directly, and use the ``invite``
            method.

        Any user that is to be added to an organization, must be added
        to a team as per the GitHub api.

        .. note::
            This method is of complexity O(n). This iterates over all teams in
            your organization and only adds the user when the team name
            matches the team parameter above. If you want constant time, you
            should retrieve the team and call ``add_member`` on that team
            directly.

        :param str login: (required), login name of the user to be added
        :param str team: (required), team name
        :returns: bool
        """
        warnings.warn(
            'This is no longer supported by the GitHub API, see '
            'https://developer.github.com/changes/2014-09-23-one-more-week'
            '-before-the-add-team-member-api-breaking-change/',
            DeprecationWarning)
        for t in self.iter_teams():
            if team == t.name:
                return t.add_member(login)
        return False

    @requires_auth
    def add_repo(self, repo, team):
        """Add ``repo`` to ``team``.

        .. note::
            This method is of complexity O(n). This iterates over all teams in
            your organization and only adds the repo when the team name
            matches the team parameter above. If you want constant time, you
            should retrieve the team and call ``add_repo`` on that team
            directly.

        :param str repo: (required), form: 'user/repo'
        :param str team: (required), team name
        """
        for t in self.iter_teams():
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
                    team_id=0,
                    auto_init=False,
                    gitignore_template=''):
        """Create a repository for this organization if the authenticated user
        is a member.

        :param str name: (required), name of the repository
        :param str description: (optional)
        :param str homepage: (optional)
        :param bool private: (optional), If ``True``, create a private
            repository. API default: ``False``
        :param bool has_issues: (optional), If ``True``, enable issues for
            this repository. API default: ``True``
        :param bool has_wiki: (optional), If ``True``, enable the wiki for
            this repository. API default: ``True``
        :param bool has_downloads: (optional), If ``True``, enable downloads
            for this repository. API default: ``True``
        :param int team_id: (optional), id of the team that will be granted
            access to this repository
        :param bool auto_init: (optional), auto initialize the repository.
        :param str gitignore_template: (optional), name of the template; this
            is ignored if auto_int = False.
        :returns: :class:`Repository <github3.repos.Repository>`

        .. warning: ``name`` should be no longer than 100 characters
        """
        url = self._build_url('repos', base_url=self._api)
        data = {'name': name, 'description': description,
                'homepage': homepage, 'private': private,
                'has_issues': has_issues, 'has_wiki': has_wiki,
                'has_downloads': has_downloads, 'auto_init': auto_init,
                'gitignore_template': gitignore_template}
        if team_id > 0:
            data.update({'team_id': team_id})
        json = self._json(self._post(url, data), 201)
        return Repository(json, self) if json else None

    @requires_auth
    def conceal_member(self, login):
        """Conceal ``login``'s membership in this organization.

        :returns: bool
        """
        url = self._build_url('public_members', login, base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def create_team(self, name, repo_names=[], permission=''):
        """Assuming the authenticated user owns this organization,
        create and return a new team.

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
    def edit(self,
             billing_email=None,
             company=None,
             email=None,
             location=None,
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

    def iter_events(self, number=-1, etag=None):
        """Iterate over events for this org.

        :param int number: (optional), number of events to return. Default: -1
            iterates over all events available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def iter_members(self, number=-1, etag=None):
        """Iterate over members of this organization.

        :param int number: (optional), number of members to return. Default:
            -1 will return all available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def iter_public_members(self, number=-1, etag=None):
        """Iterate over public members of this organization.

        :param int number: (optional), number of members to return. Default:
            -1 will return all available.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('public_members', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def iter_repos(self, type='', number=-1, etag=None):
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
    def iter_teams(self, number=-1, etag=None):
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
        for t in self.iter_teams():
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


class Membership(GitHubCore):

    """The wrapper for information about Team and Organization memberships."""

    def __init__(self, membership, session=None):
        super(Membership, self).__init__(membership, session)
        self._update_attributes(membership)

    def _repr(self):
        return '<Membership [{0}]>'.format(self.organization)

    def _update_attributes(self, membership):
        self._api = membership.get('url')
        self.organization = Organization(membership.get('organization', {}),
                                         self)
        self.state = membership.get('state', '')
        self.organization_url = membership.get('organization_url')
        self.active = self.state.lower() == 'active'
        self.pending = self.state.lower() == 'pending'

    @requires_auth
    def edit(self, state):
        """Edit the user's membership.

        :param str state: (required), the state the membership should be in.
            Only accepts ``"active"``.
        :returns: itself
        """
        if state and state.lower() == 'active':
            data = dumps({'state': state.lower()})
            json = self._json(self._patch(self._api, data=data))
            self._update_attributes(json)
        return self
