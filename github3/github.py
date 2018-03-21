# -*- coding: utf-8 -*-
"""This module contains the main interfaces to the API."""
from __future__ import unicode_literals

import json
import re

import uritemplate

from . import auths
from . import events
from . import gists
from . import issues
from . import licenses
from . import models
from . import notifications
from . import orgs
from . import projects
from . import pulls
from .repos import repo
from . import search
from . import structs
from . import users

from .decorators import (requires_auth, requires_basic_auth,
                         requires_app_credentials)


_pubsub_re = re.compile(
    'https?://[\w\d\-\.\:]+/\w[\w-]+\w/[\w\._-]+/events/\w+'
)


class GitHub(models.GitHubCore):
    """Stores all the session information.

    There are two ways to log into the GitHub API

    .. code-block:: python

        from github3 import login
        g = login(user, password)
        g = login(token=token)
        g = login(user, token=token)

    or

    .. code-block:: python

        from github3 import GitHub
        g = GitHub(user, password)
        g = GitHub(token=token)
        g = GitHub(user, token=token)

    This is simple backward compatibility since originally there was no way to
    call the GitHub object with authentication parameters.
    """

    def __init__(self, username='', password='', token=''):
        """Create a new GitHub instance to talk to the API."""
        super(GitHub, self).__init__({}, self.new_session())
        if token:
            self.login(username, token=token)
        elif username and password:
            self.login(username, password)

    def _repr(self):
        if self.session.auth:
            return '<GitHub [{0[0]}]>'.format(self.session.auth)
        return '<Anonymous GitHub at 0x{0:x}>'.format(id(self))

    @requires_auth
    def add_email_addresses(self, addresses=[]):
        """Add the addresses to the authenticated user's account.

        :param list addresses:
            (optional), email addresses to be added
        :returns:
            list of email objects
        :rtype:
            [:class:`~github3.users.Email`]
        """
        json = []
        if addresses:
            url = self._build_url('user', 'emails')
            json = self._json(self._post(url, data=addresses), 201)
        return [users.Email(email, self) for email in json] if json else []

    def all_events(self, number=-1, etag=None):
        """Iterate over public events.

        :param int number:
            (optional), number of events to return. Default: -1
            returns all available events
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of events
        :rtype:
            :class:`~github3.events.Event`
        """
        url = self._build_url('events')
        return self._iter(int(number), url, events.Event, etag=etag)

    def all_organizations(self, number=-1, since=None, etag=None,
                          per_page=None):
        """Iterate over every organization in the order they were created.

        :param int number:
            (optional), number of organizations to return.
            Default: -1, returns all of them
        :param int since:
            (optional), last organization id seen (allows restarting an
            iteration)
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :param int per_page:
            (optional), number of organizations to list per request
        :returns:
            generator of organizations
        :rtype:
            :class:`~github3.orgs.ShortOrganization`
        """
        url = self._build_url('organizations')
        return self._iter(int(number), url, orgs.ShortOrganization,
                          params={'since': since, 'per_page': per_page},
                          etag=etag)

    def all_repositories(self, number=-1, since=None, etag=None,
                         per_page=None):
        """Iterate over every repository in the order they were created.

        :param int number:
            (optional), number of repositories to return.
            Default: -1, returns all of them
        :param int since:
            (optional), last repository id seen (allows restarting an
            iteration)
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :param int per_page:
            (optional), number of repositories to list per request
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        url = self._build_url('repositories')
        return self._iter(int(number), url, repo.ShortRepository,
                          params={'since': since, 'per_page': per_page},
                          etag=etag)

    def all_users(self, number=-1, etag=None, per_page=None, since=None):
        """Iterate over every user in the order they signed up for GitHub.

        .. versionchanged:: 1.0.0

            Inserted the ``since`` parameter after the ``number`` parameter.

        :param int number:
            (optional), number of users to return. Default: -1, returns all of
            them
        :param int since:
            (optional), ID of the last user that you've seen.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :param int per_page:
            (optional), number of users to list per request
        :returns:
            generator of users
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        url = self._build_url('users')
        return self._iter(int(number), url, users.ShortUser, etag=etag,
                          params={'per_page': per_page, 'since': since})

    @requires_basic_auth
    def authorization(self, id_num):
        """Get information about authorization ``id``.

        :param int id_num:
            (required), unique id of the authorization
        :returns:
            :class:`~github3.auths.Authorization`
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('authorizations', str(id_num))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(auths.Authorization, json)

    @requires_basic_auth
    def authorizations(self, number=-1, etag=None):
        """Iterate over authorizations for the authenticated user.

        .. note::

            This will return a 404 if you are using a token for
            authentication.

        :param int number:
            (optional), number of authorizations to return.
            Default: -1 returns all available authorizations
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of authorizations
        :rtype:
            :class:`~github3.auths.Authorization`
        """
        url = self._build_url('authorizations')
        return self._iter(int(number), url, auths.Authorization, etag=etag)

    def authorize(self, username, password, scopes=None, note='', note_url='',
                  client_id='', client_secret=''):
        """Obtain an authorization token.

        The retrieved token will allow future consumers to use the API without
        a username and password.

        :param str username:
            (required)
        :param str password:
            (required)
        :param list scopes:
            (optional), areas you want this token to apply to, i.e., 'gist',
            'user'
        :param str note:
            (optional), note about the authorization
        :param str note_url:
            (optional), url for the application
        :param str client_id:
            (optional), 20 character OAuth client key for which to create a
            token
        :param str client_secret:
            (optional), 40 character OAuth client secret for which to create
            the token
        :returns:
            created authorization
        :rtype:
            :class:`~github3.auths.Authorization`
        """
        json = None

        if username and password:
            url = self._build_url('authorizations')
            data = {'note': note, 'note_url': note_url,
                    'client_id': client_id, 'client_secret': client_secret}
            if scopes:
                data['scopes'] = scopes

            with self.session.temporary_basic_auth(username, password):
                json = self._json(self._post(url, data=data), 201)

        return self._instance_or_null(auths.Authorization, json)

    def check_authorization(self, access_token):
        """Check an authorization created by a registered application.

        OAuth applications can use this method to check token validity
        without hitting normal rate limits because of failed login attempts.
        If the token is valid, it will return True, otherwise it will return
        False.

        :returns:
            True if token is valid, False otherwise
        :rtype:
            bool
        """
        p = self.session.params
        auth = (p.get('client_id'), p.get('client_secret'))
        if access_token and auth:
            url = self._build_url('applications', str(auth[0]), 'tokens',
                                  str(access_token))
            resp = self._get(url, auth=auth, params={
                'client_id': None, 'client_secret': None
            })
            return self._boolean(resp, 200, 404)
        return False

    @requires_auth
    def create_gist(self, description, files, public=True):
        """Create a new gist.

        .. versionchanged:: 1.1.0

            Per `GitHub's recent announcement`_ authentication is now required
            for creating gists.

        .. _GitHub's recent announcement:
            https://blog.github.com/2018-02-18-deprecation-notice-removing-anonymous-gist-creation/

        :param str description:
            (required), description of gist
        :param dict files:
            (required), file names with associated dictionaries for content,
            e.g. ``{'spam.txt': {'content': 'File contents ...'}}``
        :param bool public:
            (optional), make the gist public if True
        :returns:
            the created gist if successful, otherwise ``None``
        :rtype:
            created gist
        :rtype:
            :class:`~github3.gists.gist.Gist`
        """
        new_gist = {'description': description, 'public': public,
                    'files': files}
        url = self._build_url('gists')
        json = self._json(self._post(url, data=new_gist), 201)
        return self._instance_or_null(gists.Gist, json)

    @requires_auth
    def create_issue(self, owner, repository, title, body=None, assignee=None,
                     milestone=None, labels=[], assignees=None):
        """Create an issue on the repository.

        .. note::

            ``body``, ``assignee``, ``assignees``, ``milestone``, ``labels``
            are all optional.

        .. warning::

            This method retrieves the repository first and then uses it to
            create an issue. If you're making several issues, you should use
            :py:meth:`repository <github3.github.GitHub.repository>` and then
            use :py:meth:`create_issue
            <github3.repos.repo.Repository.create_issue>`

        :param str owner:
            (required), login of the owner
        :param str repository:
            (required), repository name
        :param str title:
            (required), Title of issue to be created
        :param str body:
            (optional), The text of the issue, markdown formatted
        :param str assignee:
            (optional), Login of person to assign the issue to
        :param assignees:
            (optional), logins of the users to assign the issue to
        :param int milestone:
            (optional), id number of the milestone to attribute this issue to
            (e.g. if ``m`` is a :class:`~github3.issues.Milestone` object,
            ``m.number`` is what you pass here.)
        :param list labels:
            (optional), List of label names.
        :returns:
            created issue
        :rtype:
            :class:`~github3.issues.ShortIssue`
        """
        repo = None
        if owner and repository and title:
            repo = self.repository(owner, repository)

        if repo is not None:
            return repo.create_issue(title, body, assignee, milestone,
                                     labels, assignees)

        return self._instance_or_null(issues.ShortIssue, None)

    @requires_auth
    def create_key(self, title, key, read_only=False):
        """Create a new key for the authenticated user.

        :param str title:
            (required), key title
        :param str key:
            (required), actual key contents, accepts path
            as a string or file-like object
        :param bool read_only:
            (optional), restrict key access to read-only, default to False
        :returns:
            created key
        :rtype:
            :class:`~github3.users.Key`
        """
        json = None

        if title and key:
            data = {'title': title, 'key': key, 'read_only': read_only}
            url = self._build_url('user', 'keys')
            req = self._post(url, data=data)
            json = self._json(req, 201)
        return self._instance_or_null(users.Key, json)

    @requires_auth
    def create_repository(self, name, description='', homepage='',
                          private=False, has_issues=True, has_wiki=True,
                          auto_init=False, gitignore_template=''):
        """Create a repository for the authenticated user.

        :param str name:
            (required), name of the repository

            .. warning: this be no longer than 100 characters
        :param str description:
            (optional)
        :param str homepage:
            (optional)
        :param str private:
            (optional), If ``True``, create a private repository. API default:
            ``False``
        :param bool has_issues:
            (optional), If ``True``, enable issues for this repository. API
            default: ``True``
        :param bool has_wiki:
            (optional), If ``True``, enable the wiki for this repository. API
            default: ``True``
        :param bool auto_init:
            (optional), auto initialize the repository
        :param str gitignore_template:
            (optional), name of the git template to use; ignored if auto_init =
            False.
        :returns:
            created repository
        :rtype:
            :class:`~github3.repos.repo.Repository`
        """
        url = self._build_url('user', 'repos')
        data = {'name': name, 'description': description,
                'homepage': homepage, 'private': private,
                'has_issues': has_issues, 'has_wiki': has_wiki,
                'auto_init': auto_init,
                'gitignore_template': gitignore_template}
        json = self._json(self._post(url, data=data), 201)
        return self._instance_or_null(repo.Repository, json)

    @requires_auth
    def delete_email_addresses(self, addresses=[]):
        """Delete the specified addresses the authenticated user's account.

        :param list addresses:
            (optional), email addresses to be removed
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        url = self._build_url('user', 'emails')
        return self._boolean(self._delete(url, data=json.dumps(addresses)),
                             204, 404)

    @requires_auth
    def emails(self, number=-1, etag=None):
        """Iterate over email addresses for the authenticated user.

        :param int number:
            (optional), number of email addresses to return.
            Default: -1 returns all available email addresses
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of emails
        :rtype:
            :class:`~github3.users.Email`
        """
        url = self._build_url('user', 'emails')
        return self._iter(int(number), url, users.Email, etag=etag)

    def emojis(self):
        """Retrieve a dictionary of all of the emojis that GitHub supports.

        :returns:
            dictionary where the key is what would be in between the
            colons and the value is the URL to the image, e.g.,

            .. code-block:: python

                {
                    '+1': 'https://github.global.ssl.fastly.net/images/...',
                    # ...
                }
        """
        url = self._build_url('emojis')
        return self._json(self._get(url), 200, include_cache_info=False)

    @requires_basic_auth
    def feeds(self):
        """List GitHub's timeline resources in Atom format.

        :returns:
            dictionary parsed to include URITemplates
        :rtype:
            dict
        """
        def replace_href(feed_dict):
            if not feed_dict:
                return feed_dict
            ret_dict = {}
            # Let's pluck out what we're most interested in, the href value
            href = feed_dict.pop('href', None)
            # Then we update the return dictionary with the rest of the values
            ret_dict.update(feed_dict)
            if href is not None:
                # So long as there is something to template, let's template it
                ret_dict['href'] = uritemplate.URITemplate(href)
            return ret_dict

        url = self._build_url('feeds')
        json = self._json(self._get(url), 200, include_cache_info=False)
        if json is None:  # If something went wrong, get out early
            return None

        # We have a response body to parse
        feeds = {}

        # Let's pop out the old links so we don't have to skip them below
        old_links = json.pop('_links', {})
        _links = {}
        # If _links is in the response JSON, iterate over that and recreate it
        # so that any templates contained inside can be turned into
        # URITemplates
        for key, value in old_links.items():
            if isinstance(value, list):
                # If it's an array/list of links, let's replace that with a
                # new list of links
                _links[key] = [replace_href(d) for d in value]
            else:
                # Otherwise, just use the new value
                _links[key] = replace_href(value)

        # Start building up our return dictionary
        feeds['_links'] = _links

        for key, value in json.items():
            # This should roughly be the same logic as above.
            if isinstance(value, list):
                feeds[key] = [uritemplate.URITemplate(v) for v in value]
            else:
                feeds[key] = uritemplate.URITemplate(value)

        return feeds

    @requires_auth
    def follow(self, username):
        """Make the authenticated user follow the provided username.

        :param str username:
            (required), user to follow
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = False
        if username:
            url = self._build_url('user', 'following', username)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    def followed_by(self, username, number=-1, etag=None):
        """Iterate over users being followed by ``username``.

        .. versionadded:: 1.0.0

            This replaces iter_following('sigmavirus24').

        :param str username:
            (required), login of the user to check
        :param int number:
            (optional), number of people to return. Default: -1 returns all
            people you follow
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of users
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        url = self._build_url('users', username, 'following')
        return self._iter(int(number), url, users.ShortUser, etag=etag)

    @requires_auth
    def followers(self, number=-1, etag=None):
        """Iterate over followers of the authenticated user.

        .. versionadded:: 1.0.0

            This replaces iter_followers().

        :param int number:
            (optional), number of followers to return. Default: -1 returns all
            followers
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of followers
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        url = self._build_url('user', 'followers')
        return self._iter(int(number), url, users.ShortUser, etag=etag)

    def followers_of(self, username, number=-1, etag=None):
        """Iterate over followers of ``username``.

        .. versionadded:: 1.0.0

            This replaces iter_followers('sigmavirus24').

        :param str username:
            (required), login of the user to check
        :param int number:
            (optional), number of followers to return. Default: -1 returns all
            followers
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of followers
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        url = self._build_url('users', username, 'followers')
        return self._iter(int(number), url, users.ShortUser, etag=etag)

    @requires_auth
    def following(self, number=-1, etag=None):
        """Iterate over users the authenticated user is following.

        .. versionadded:: 1.0.0

            This replaces iter_following().

        :param int number:
            (optional), number of people to return. Default: -1 returns all
            people you follow
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of users
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        url = self._build_url('user', 'following')
        return self._iter(int(number), url, users.ShortUser, etag=etag)

    def gist(self, id_num):
        """Retrieve the gist using the specified id number.

        :param int id_num:
            (required), unique id of the gist
        :returns:
            the gist identified by ``id_num``
        :rtype:
            :class:`~github3.gists.gist.Gist`
        """
        url = self._build_url('gists', str(id_num))
        json = self._json(self._get(url), 200)
        return self._instance_or_null(gists.Gist, json)

    @requires_auth
    def gists(self, number=-1, etag=None):
        """Retrieve the authenticated user's gists.

        .. versionadded:: 1.0

        :param int number:
            (optional), number of gists to return. Default: -1, returns all
            available gists
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of short gists
        :rtype:
            :class:~github3.gists.ShortGist`
        """
        url = self._build_url('gists')
        return self._iter(int(number), url, gists.ShortGist, etag=etag)

    def gists_by(self, username, number=-1, etag=None):
        """Iterate over the gists owned by a user.

        .. versionadded:: 1.0

        :param str username:
            login of the user who owns the gists
        :param int number:
            (optional), number of gists to return. Default: -1 returns all
            available gists
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of short gists owned by the specified user
        :rtype:
            :class:`~github3.gists.ShortGist`
        """
        url = self._build_url('users', username, 'gists')
        return self._iter(int(number), url, gists.ShortGist, etag=etag)

    def gitignore_template(self, language):
        """Return the template for language.

        :returns:
            the template string
        :rtype:
            str
        """
        url = self._build_url('gitignore', 'templates', language)
        json = self._json(self._get(url), 200)
        if not json:
            return ''
        return json.get('source', '')

    def gitignore_templates(self):
        """Return the list of available templates.

        :returns:
            list of template names
        :rtype:
            [str]
        """
        url = self._build_url('gitignore', 'templates')
        return self._json(self._get(url), 200) or []

    @requires_auth
    def is_following(self, username):
        """Check if the authenticated user is following login.

        :param str username:
            (required), login of the user to check if the
            authenticated user is checking
        :returns:
            True if following, False otherwise
        :rtype:
            bool
        """
        json = False
        if username:
            url = self._build_url('user', 'following', username)
            json = self._boolean(self._get(url), 204, 404)
        return json

    @requires_auth
    def is_starred(self, username, repo):
        """Check if the authenticated user starred username/repo.

        :param str username:
            (required), owner of repository
        :param str repo:
            (required), name of repository
        :returns:
            True if starred, False otherwise
        :rtype:
            bool
        """
        json = False
        if username and repo:
            url = self._build_url('user', 'starred', username, repo)
            json = self._boolean(self._get(url), 204, 404)
        return json

    def issue(self, username, repository, number):
        """Fetch issue from owner/repository.

        :param str username:
            (required), owner of the repository
        :param str repository:
            (required), name of the repository
        :param int number:
            (required), issue number
        :return:
            the issue
        :rtype:
            :class:`~github3.issues.issue.Issue`
        """
        json = None
        if username and repository and int(number) > 0:
            url = self._build_url('repos', username, repository, 'issues',
                                  str(number))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(issues.Issue, json)

    @requires_auth
    def issues(self, filter='', state='', labels='', sort='', direction='',
               since=None, number=-1, etag=None):
        """List all of the authenticated user's (and organization's) issues.

        .. versionchanged:: 0.9.0

            - The ``state`` parameter now accepts 'all' in addition to 'open'
              and 'closed'.

        :param str filter:
            accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state:
            accepted values: ('all', 'open', 'closed')
            api-default: 'open'
        :param str labels:
            comma-separated list of label names, e.g., 'bug,ui,@high'
        :param str sort:
            accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction:
            accepted values: ('asc', 'desc')
            api-default: desc
        :param since:
            (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since:
            :class:`~datetime.datetime` or str
        :param int number:
            (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of issues
        :rtype:
            :class:`~github3.issues.ShortIssue`
        """
        url = self._build_url('issues')
        # issue_params will handle the since parameter
        params = issues.issue_params(
            filter, state, labels, sort, direction, since
        )
        return self._iter(int(number), url, issues.ShortIssue, params, etag)

    def issues_on(self, username, repository, milestone=None, state=None,
                  assignee=None, mentioned=None, labels=None, sort=None,
                  direction=None, since=None, number=-1, etag=None):
        """List issues on owner/repository.

        Only owner and repository are required.

        .. versionchanged:: 0.9.0

            - The ``state`` parameter now accepts 'all' in addition to 'open'
              and 'closed'.

        :param str username:
            login of the owner of the repository
        :param str repository:
            name of the repository
        :param int milestone:
            None, '*', or ID of milestone
        :param str state:
            accepted values: ('all', 'open', 'closed')
            api-default: 'open'
        :param str assignee:
            '*' or login of the user
        :param str mentioned:
            login of the user
        :param str labels:
            comma-separated list of label names, e.g., 'bug,ui,@high'
        :param str sort:
            accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction:
            accepted values: ('asc', 'desc')
            api-default: desc
        :param since:
            (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since:
            :class:`~datetime.datetime` or str
        :param int number:
            (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of issues
        :rtype:
            :class:`~github3.issues.ShortIssue`
        """
        if username and repository:
            url = self._build_url('repos', username, repository, 'issues')

            params = repo.repo_issue_params(
                milestone, state, assignee, mentioned,
                labels, sort, direction, since,
            )
            return self._iter(int(number), url, issues.ShortIssue,
                              params=params, etag=etag)
        return iter([])

    @requires_auth
    def key(self, id_num):
        """Get the authenticated user's key specified by id_num.

        :param int id_num:
            (required), unique id of the key
        :returns:
            created key
        :rtype:
            :class:`~github3.users.Key`
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('user', 'keys', str(id_num))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(users.Key, json)

    @requires_auth
    def keys(self, number=-1, etag=None):
        """Iterate over public keys for the authenticated user.

        :param int number:
            (optional), number of keys to return. Default: -1
            returns all your keys
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of keys
        :rtype:
            :class:`~github3.users.Key`
        """
        url = self._build_url('user', 'keys')
        return self._iter(int(number), url, users.Key, etag=etag)

    def license(self, name):
        """Retrieve the license specified by the name.

        :param string name:
            (required), name of license
        :returns:
            the specified license
        :rtype:
            :class:`~github3.licenses.License`
        """
        url = self._build_url('licenses', name)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(licenses.License, json)

    def licenses(self, number=-1, etag=None):
        """Iterate over open source licenses.

        :returns:
            generator of short license objects
        :rtype:
            :class:`~github3.licenses.ShortLicense`
        """
        url = self._build_url('licenses')
        return self._iter(int(number), url, licenses.ShortLicense, etag=etag)

    def login(self, username=None, password=None, token=None,
              two_factor_callback=None):
        """Log the user into GitHub for protected API calls.

        :param str username:
            login name
        :param str password:
            password for the login
        :param str token:
            OAuth token
        :param func two_factor_callback:
            (optional), function you implement to provide the Two Factor
            Authentication code to GitHub when necessary
        """
        if username and password:
            self.session.basic_auth(username, password)
        elif token:
            self.session.token_auth(token)

        # The Session method handles None for free.
        self.session.two_factor_auth_callback(two_factor_callback)

    def markdown(self, text, mode='', context='', raw=False):
        """Render an arbitrary markdown document.

        :param str text:
            (required), the text of the document to render
        :param str mode:
            (optional), 'markdown' or 'gfm'
        :param str context:
            (optional), only important when using mode 'gfm', this is the
            repository to use as the context for the rendering
        :param bool raw:
            (optional), renders a document like a README.md, no gfm, no context
        :returns:
            the HTML formatted markdown text
        :rtype:
            str (or unicode on Python 2)
        """
        data = None
        json = False
        headers = {}
        if raw:
            url = self._build_url('markdown', 'raw')
            data = text
            headers['content-type'] = 'text/plain'
        else:
            url = self._build_url('markdown')
            data = {}

            if text:
                data['text'] = text

            if mode in ('markdown', 'gfm'):
                data['mode'] = mode

            if context:
                data['context'] = context
            json = True

        html = ''
        if data:
            req = self._post(url, data=data, json=json, headers=headers)
            if req.ok:
                html = req.text
        return html

    @requires_auth
    def me(self):
        """Retrieve the info for the authenticated user.

        .. versionadded:: 1.0

            This was separated from the ``user`` method.

        :returns:
            the representation of the authenticated user.
        :rtype:
            :class:`~github3.users.AuthenticatedUser`
        """
        url = self._build_url('user')
        json = self._json(self._get(url), 200)
        return self._instance_or_null(users.AuthenticatedUser, json)

    @requires_auth
    def membership_in(self, organization):
        """Retrieve the user's membership in the specified organization.

        :param organization:
            the organization or organization login to retrieve the authorized
            user's membership in
        :type organization:
            str
        :type organization:
            :class:`~github3.orgs.Organization`
        :returns:
            the user's membership
        :rtype:
            :class:`~github3.orgs.Membership`
        """
        organization_name = getattr(organization, 'login', organization)
        url = self._build_url('user', 'memberships', 'orgs', organization_name)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(orgs.Membership, json)

    def meta(self):
        """Retrieve a dictionary with arrays of addresses in CIDR format.

        The addresses in CIDR format specify the addresses that the incoming
        service hooks will originate from.

        .. versionadded:: 0.5

        :returns:
            CIDR addresses
        :rtype:
            dict
        """
        url = self._build_url('meta')
        return self._json(self._get(url), 200) or {}

    @requires_auth
    def notifications(self, all=False, participating=False, number=-1,
                      etag=None):
        """Iterate over the user's notification.

        :param bool all:
            (optional), iterate over all notifications
        :param bool participating:
            (optional), only iterate over notifications in which the user is
            participating
        :param int number:
            (optional), how many notifications to return
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of threads
        :rtype:
            :class:`~github3.notifications.Thread`
        """
        params = None
        if all is True:
            params = {'all': 'true'}
        elif participating is True:
            params = {'participating': 'true'}

        url = self._build_url('notifications')
        return self._iter(
            int(number), url, notifications.Thread, params, etag=etag
        )

    def octocat(self, say=None):
        """Return an easter egg of the API.

        :params str say:
            (optional), pass in what you'd like Octocat to say
        :returns:
            ascii art of Octocat
        :rtype:
            str (or unicode on Python 2)
        """
        url = self._build_url('octocat')
        req = self._get(url, params={'s': say})
        return req.text if req.ok else ''

    def organization(self, username):
        """Return an Organization object for the login name.

        :param str username:
            (required), login name of the org
        :returns:
            the organization
        :rtype:
            :class:`~github3.orgs.Organization`
        """
        url = self._build_url('orgs', username)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(orgs.Organization, json)

    @requires_auth
    def organization_issues(self, name, filter='', state='', labels='',
                            sort='', direction='', since=None, number=-1,
                            etag=None):
        """Iterate over the organization's issues.

        .. note::

            This only works if the authenticated user belongs to it.

        :param str name:
            (required), name of the organization
        :param str filter:
            accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state:
            accepted values: ('open', 'closed')
            api-default: 'open'
        :param str labels:
            comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort:
            accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction:
            accepted values: ('asc', 'desc')
            api-default: desc
        :param since:
            (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since:
            :class:`~datetime.datetime` or str
        :param int number:
            (optional), number of issues to return. Default:
            -1, returns all available issues
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of issues
        :rtype:
            :class:`~github3.issues.ShortIssue`
        """
        url = self._build_url('orgs', name, 'issues')
        # issue_params will handle the since parameter
        params = issues.issue_params(
            filter, state, labels, sort, direction, since
        )
        return self._iter(int(number), url, issues.ShortIssue, params, etag)

    @requires_auth
    def organizations(self, number=-1, etag=None):
        """Iterate over all organizations the authenticated user belongs to.

        This will display both the private memberships and the publicized
        memberships.

        :param int number:
            (optional), number of organizations to return.
            Default: -1 returns all available organizations
        :param str etag:
            (optional), ETag from a previous request to the same
            endpoint
        :returns:
            generator of organizations
        :rtype:
            :class:`~github3.orgs.ShortOrganization`
        """
        url = self._build_url('user', 'orgs')
        return self._iter(int(number), url, orgs.ShortOrganization, etag=etag)

    def organizations_with(self, username, number=-1, etag=None):
        """Iterate over organizations with ``username`` as a public member.

        .. versionadded:: 1.0.0

            Replaces ``iter_orgs('sigmavirus24')``.

        :param str username:
            (optional), user whose orgs you wish to list
        :param int number:
            (optional), number of organizations to return.
            Default: -1 returns all available organizations
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of organizations
        :rtype:
            :class:`~github3.orgs.ShortOrganization`
        """
        if username:
            url = self._build_url('users', username, 'orgs')
            return self._iter(int(number), url, orgs.ShortOrganization,
                              etag=etag)
        return iter([])

    def project(self, number):
        """Return the Project with id ``number``.

        :param int number:
            id of the project
        :returns:
            the project
        :rtype:
            :class:`~github3.projects.Project`
        """
        number = int(number)
        json = None
        if number > 0:
            url = self._build_url('projects', str(number))
            json = self._json(self._get(
                url, headers=projects.Project.CUSTOM_HEADERS), 200)
        return self._instance_or_null(projects.Project, json)

    def project_card(self, number):
        """Return the ProjectCard with id ``number``.

        :param int number:
            id of the project card
        :returns:
            :class:`~github3.projects.ProjectCard`
        """
        number = int(number)
        json = None
        if number > 0:
            url = self._build_url('projects', 'columns', 'cards', str(number))
            json = self._json(self._get(
                url, headers=projects.Project.CUSTOM_HEADERS), 200)
        return self._instance_or_null(projects.ProjectCard, json)

    def project_column(self, number):
        """Return the ProjectColumn with id ``number``.

        :param int number:
            id of the project column
        :returns:
            :class:`~github3.projects.ProjectColumn`
        """
        number = int(number)
        json = None
        if number > 0:
            url = self._build_url('projects', 'columns', str(number))
            json = self._json(self._get(
                url, headers=projects.Project.CUSTOM_HEADERS), 200)
        return self._instance_or_null(projects.ProjectColumn, json)

    def public_gists(self, number=-1, etag=None):
        """Retrieve all public gists and iterate over them.

        .. versionadded:: 1.0

        :param int number:
            (optional), number of gists to return. Default: -1
            returns all available gists
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of short gists
        :rtype:
            :class:`~github3.gists.gist.ShortGist`
        """
        url = self._build_url('gists', 'public')
        return self._iter(int(number), url, gists.ShortGist, etag=etag)

    @requires_auth
    def organization_memberships(self, state=None, number=-1, etag=None):
        """List organizations of which the user is a current or pending member.

        :param str state:
            (option), state of the membership, i.e., active, pending
        :returns:
            iterator of memberships
        :rtype:
            :class:`~github3.orgs.Membership`
        """
        params = None
        url = self._build_url('user', 'memberships', 'orgs')
        if state is not None and state.lower() in ('active', 'pending'):
            params = {'state': state.lower()}
        return self._iter(int(number), url, orgs.Membership,
                          params=params,
                          etag=etag)

    @requires_auth
    def pubsubhubbub(self, mode, topic, callback, secret=''):
        """Create or update a pubsubhubbub hook.

        :param str mode:
            (required), accepted values: ('subscribe', 'unsubscribe')
        :param str topic:
            (required), form: https://github.com/:user/:repo/events/:event
        :param str callback:
            (required), the URI that receives the updates
        :param str secret:
            (optional), shared secret key that generates a
            SHA1 HMAC of the payload content.
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        m = _pubsub_re.match(topic)
        status = False
        if mode and topic and callback and m:
            data = [('hub.mode', mode), ('hub.topic', topic),
                    ('hub.callback', callback)]
            if secret:
                data.append(('hub.secret', secret))
            url = self._build_url('hub')
            # This is not JSON data. It is meant to be form data
            # application/x-www-form-urlencoded works fine here, no need for
            # multipart/form-data
            status = self._boolean(self._post(url, data=data, json=False,
                                   headers={
                                       'Content-Type':
                                       'application/x-www-form-urlencoded'
                                   }), 204, 404)
        return status

    def pull_request(self, owner, repository, number):
        """Fetch pull_request #:number: from :owner:/:repository.

        :param str owner:
            (required), owner of the repository
        :param str repository:
            (required), name of the repository
        :param int number:
            (required), issue number
        :return:
            :class:`~github.pulls.PullRequest`
        """
        json = None
        if int(number) > 0:
            url = self._build_url('repos', owner, repository, 'pulls',
                                  str(number))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(pulls.PullRequest, json)

    def rate_limit(self):
        """Return a dictionary with information from /rate_limit.

        The dictionary has two keys: ``resources`` and ``rate``. In
        ``resources`` you can access information about ``core`` or ``search``.

        Note: the ``rate`` key will be deprecated before version 3 of the
        GitHub API is finalized. Do not rely on that key. Instead, make your
        code future-proof by using ``core`` in ``resources``, e.g.,

        .. code-block:: python

            rates = g.rate_limit()
            rates['resources']['core']  # => your normal ratelimit info
            rates['resources']['search']  # => your search ratelimit info

        .. versionadded:: 0.8

        :returns:
            ratelimit mapping
        :rtype:
            dict
        """
        url = self._build_url('rate_limit')
        return self._json(self._get(url), 200)

    @requires_auth
    def repositories(self, type=None, sort=None, direction=None, number=-1,
                     etag=None):
        """List repositories for the authenticated user, filterable by ``type``.

        .. versionchanged:: 0.6

           Removed the login parameter for correctness. Use repositories_by
           instead

        :param str type:
            (optional), accepted values:
            ('all', 'owner', 'public', 'private', 'member')
            API default: 'all'
        :param str sort:
            (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :param str direction:
            (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        url = self._build_url('user', 'repos')

        params = {}
        if type in ('all', 'owner', 'public', 'private', 'member'):
            params.update(type=type)
        if sort in ('created', 'updated', 'pushed', 'full_name'):
            params.update(sort=sort)
        if direction in ('asc', 'desc'):
            params.update(direction=direction)

        return self._iter(int(number), url, repo.ShortRepository, params,
                          etag)

    def repositories_by(self, username, type=None, sort=None, direction=None,
                        number=-1, etag=None):
        """List public repositories for the specified ``username``.

        .. versionadded:: 0.6

        :param str username:
            (required), username
        :param str type:
            (optional), accepted values: ('all', 'owner', 'member')
            API default: 'all'
        :param str sort:
            (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :param str direction:
            (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        url = self._build_url('users', username, 'repos')

        params = {}
        if type in ('all', 'owner', 'member'):
            params.update(type=type)
        if sort in ('created', 'updated', 'pushed', 'full_name'):
            params.update(sort=sort)
        if direction in ('asc', 'desc'):
            params.update(direction=direction)

        return self._iter(int(number), url, repo.ShortRepository, params,
                          etag)

    def repository(self, owner, repository):
        """Retrieve the desired repository.

        :param str owner:
            (required)
        :param str repository:
            (required)
        :returns:
            the repository
        :rtype:
            :class:`~github3.repos.repo.Repository`
        """
        json = None
        if owner and repository:
            url = self._build_url('repos', owner, repository)
            json = self._json(self._get(url), 200)
        return self._instance_or_null(repo.Repository, json)

    def repository_with_id(self, number):
        """Retrieve the repository with the globally unique id.

        :param int number:
            id of the repository
        :returns:
            the repository
        :rtype:
            :class:`~github3.repos.repo.Repository`
        """
        number = int(number)
        json = None
        if number > 0:
            url = self._build_url('repositories', str(number))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(repo.Repository, json)

    @requires_app_credentials
    def revoke_authorization(self, access_token):
        """Revoke specified authorization for an OAuth application.

        Revoke all authorization tokens created by your application. This will
        only work if you have already called ``set_client_id``.

        :param str access_token:
            (required), the access_token to revoke
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        client_id, client_secret = self.session.retrieve_client_credentials()
        url = self._build_url('applications', str(client_id), 'tokens',
                              access_token)
        with self.session.temporary_basic_auth(client_id, client_secret):
            response = self._delete(url, params={'client_id': None,
                                                 'client_secret': None})

        return self._boolean(response, 204, 404)

    @requires_app_credentials
    def revoke_authorizations(self):
        """Revoke all authorizations for an OAuth application.

        Revoke all authorization tokens created by your application. This will
        only work if you have already called ``set_client_id``.

        :param str client_id:
            (required), the client_id of your application
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        client_id, client_secret = self.session.retrieve_client_credentials()
        url = self._build_url('applications', str(client_id), 'tokens')
        with self.session.temporary_basic_auth(client_id, client_secret):
            response = self._delete(url, params={'client_id': None,
                                                 'client_secret': None})

        return self._boolean(response, 204, 404)

    def search_code(self, query, sort=None, order=None, per_page=None,
                    text_match=False, number=-1, etag=None):
        """Find code via the code search API.

        The query can contain any combination of the following supported
        qualifiers:

        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the file contents, the file path, or
          both.
        - ``language`` Searches code based on the language it’s written in.
        - ``fork`` Specifies that code from forked repositories should be
          searched.  Repository forks will not be searchable unless the fork
          has more stars than the parent repository.
        - ``size`` Finds files that match a certain size (in bytes).
        - ``path`` Specifies the path that the resulting file must be at.
        - ``extension`` Matches files with a certain extension.
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.

        For more information about these qualifiers, see: http://git.io/-DvAuA

        :param str query:
            (required), a valid query as described above, e.g.,
            ``addClass in:file language:js repo:jquery/jquery``
        :param str sort:
            (optional), how the results should be sorted;
            option(s): ``indexed``; default: best match
        :param str order:
            (optional), the direction of the sorted results,
            options: ``asc``, ``desc``; default: ``desc``
        :param int per_page:
            (optional)
        :param bool text_match:
            (optional), if True, return matching search
            terms. See http://git.io/iRmJxg for more information
        :param int number:
            (optional), number of repositories to return.
            Default: -1, returns all available repositories
        :param str etag:
            (optional), previous ETag header value
        :return:
            generator of code search results
        :rtype:
            :class:`~github3.search.code.CodeSearchResult`
        """
        params = {'q': query}
        headers = {}

        if sort == 'indexed':
            params['sort'] = sort

        if sort and order in ('asc', 'desc'):
            params['order'] = order

        if text_match:
            headers = {
                'Accept': 'application/vnd.github.v3.full.text-match+json'
                }

        url = self._build_url('search', 'code')
        return structs.SearchIterator(
            number, url, search.CodeSearchResult, self, params, etag, headers
        )

    def search_issues(self, query, sort=None, order=None, per_page=None,
                      text_match=False, number=-1, etag=None):
        """Find issues by state and keyword.

        The query can contain any combination of the following supported
        qualifers:

        - ``type`` With this qualifier you can restrict the search to issues
          or pull request only.
        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the title, body, comments, or any
          combination of these.
        - ``author`` Finds issues created by a certain user.
        - ``assignee`` Finds issues that are assigned to a certain user.
        - ``mentions`` Finds issues that mention a certain user.
        - ``commenter`` Finds issues that a certain user commented on.
        - ``involves`` Finds issues that were either created by a certain user,
          assigned to that user, mention that user, or were commented on by
          that user.
        - ``state`` Filter issues based on whether they’re open or closed.
        - ``labels`` Filters issues based on their labels.
        - ``language`` Searches for issues within repositories that match a
          certain language.
        - ``created`` or ``updated`` Filters issues based on times of creation,
          or when they were last updated.
        - ``comments`` Filters issues based on the quantity of comments.
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.

        For more information about these qualifiers, see: http://git.io/d1oELA

        :param str query:
            (required), a valid query as described above, e.g.,
            ``windows label:bug``
        :param str sort:
            (optional), how the results should be sorted;
            options: ``created``, ``comments``, ``updated``;
            default: best match
        :param str order:
            (optional), the direction of the sorted results,
            options: ``asc``, ``desc``; default: ``desc``
        :param int per_page:
            (optional)
        :param bool text_match:
            (optional), if True, return matching search terms.
            See http://git.io/QLQuSQ for more information
        :param int number:
            (optional), number of issues to return.
            Default: -1, returns all available issues
        :param str etag:
            (optional), previous ETag header value
        :return:
            generator of issue search results
        :rtype:
            :class:`~github3.search.issue.IssueSearchResult`
        """
        params = {'q': query}
        headers = {}

        if sort in ('comments', 'created', 'updated'):
            params['sort'] = sort

        if order in ('asc', 'desc'):
            params['order'] = order

        if text_match:
            headers = {
                'Accept': 'application/vnd.github.v3.full.text-match+json'
                }

        url = self._build_url('search', 'issues')
        return structs.SearchIterator(
            number, url, search.IssueSearchResult, self, params, etag, headers
        )

    def search_repositories(self, query, sort=None, order=None,
                            per_page=None, text_match=False, number=-1,
                            etag=None):
        """Find repositories via various criteria.

        The query can contain any combination of the following supported
        qualifers:

        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the repository name, description,
          readme, or any combination of these.
        - ``size`` Finds repositories that match a certain size (in
          kilobytes).
        - ``forks`` Filters repositories based on the number of forks, and/or
          whether forked repositories should be included in the results at
          all.
        - ``created`` or ``pushed`` Filters repositories based on times of
          creation, or when they were last updated. Format: ``YYYY-MM-DD``.
          Examples: ``created:<2011``, ``pushed:<2013-02``,
          ``pushed:>=2013-03-06``
        - ``user`` or ``repo`` Limits searches to a specific user or
          repository.
        - ``language`` Searches repositories based on the language they're
          written in.
        - ``stars`` Searches repositories based on the number of stars.

        For more information about these qualifiers, see: http://git.io/4Z8AkA

        :param str query:
            (required), a valid query as described above, e.g.,
            ``tetris language:assembly``
        :param str sort:
            (optional), how the results should be sorted;
            options: ``stars``, ``forks``, ``updated``; default: best match
        :param str order:
            (optional), the direction of the sorted results,
            options: ``asc``, ``desc``; default: ``desc``
        :param int per_page:
            (optional)
        :param bool text_match:
            (optional), if True, return matching search
            terms. See http://git.io/4ct1eQ for more information
        :param int number:
            (optional), number of repositories to return.
            Default: -1, returns all available repositories
        :param str etag:
            (optional), previous ETag header value
        :return:
            generator of repository search results
        :rtype:
            :class:`~github3.search.repository.RepositorySearchResult`
        """
        params = {'q': query}
        headers = {}

        if sort in ('stars', 'forks', 'updated'):
            params['sort'] = sort

        if order in ('asc', 'desc'):
            params['order'] = order

        if text_match:
            headers = {
                'Accept': 'application/vnd.github.v3.full.text-match+json'
                }

        url = self._build_url('search', 'repositories')
        return structs.SearchIterator(
            number, url, search.RepositorySearchResult, self, params, etag,
            headers
        )

    def search_users(self, query, sort=None, order=None, per_page=None,
                     text_match=False, number=-1, etag=None):
        """Find users via the Search API.

        The query can contain any combination of the following supported
        qualifers:


        - ``type`` With this qualifier you can restrict the search to just
          personal accounts or just organization accounts.
        - ``in`` Qualifies which fields are searched. With this qualifier you
          can restrict the search to just the username, public email, full
          name, or any combination of these.
        - ``repos`` Filters users based on the number of repositories they
          have.
        - ``location`` Filter users by the location indicated in their
          profile.
        - ``language`` Search for users that have repositories that match a
          certain language.
        - ``created`` Filter users based on when they joined.
        - ``followers`` Filter users based on the number of followers they
          have.

        For more information about these qualifiers see: http://git.io/wjVYJw

        :param str query:
            (required), a valid query as described above, e.g.,
            ``tom repos:>42 followers:>1000``
        :param str sort:
            (optional), how the results should be sorted;
            options: ``followers``, ``repositories``, or ``joined``; default:
            best match
        :param str order:
            (optional), the direction of the sorted results,
            options: ``asc``, ``desc``; default: ``desc``
        :param int per_page:
            (optional)
        :param bool text_match:
            (optional), if True, return matching search
            terms. See http://git.io/_V1zRwa for more information
        :param int number:
            (optional), number of search results to return;
            Default: -1 returns all available
        :param str etag:
            (optional), ETag header value of the last request.
        :return:
            generator of user search results
        :rtype:
            :class:`~github3.search.user.UserSearchResult`
        """
        params = {'q': query}
        headers = {}

        if sort in ('followers', 'repositories', 'joined'):
            params['sort'] = sort

        if order in ('asc', 'desc'):
            params['order'] = order

        if text_match:
            headers = {
                'Accept': 'application/vnd.github.v3.full.text-match+json'
                }

        url = self._build_url('search', 'users')
        return structs.SearchIterator(
            number, url, search.UserSearchResult, self, params, etag, headers
        )

    def set_client_id(self, id, secret):
        """Allow the developer to set their OAuth application credentials.

        :param str id:
            20-character hexidecimal client_id provided by GitHub
        :param str secret:
            40-character hexidecimal client_secret provided by GitHub
        """
        self.session.params = {'client_id': id, 'client_secret': secret}

    def set_user_agent(self, user_agent):
        """Allow the user to set their own user agent string.

        :param str user_agent:
            string used to identify your application.
            Library default: "github3.py/{version}", e.g., "github3.py/1.0.0"
        """
        if not user_agent:
            return
        self.session.headers.update({'User-Agent': user_agent})

    @requires_auth
    def star(self, username, repo):
        """Star a repository.

        :param str username:
            (required), owner of the repo
        :param str repo:
            (required), name of the repo
        :return:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = False
        if username and repo:
            url = self._build_url('user', 'starred', username, repo)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    @requires_auth
    def starred(self, sort=None, direction=None, number=-1, etag=None):
        """Iterate over repositories starred by the authenticated user.

        .. versionchanged:: 1.0.0

           This was split from ``iter_starred`` and requires authentication.

        :param str sort:
            (optional), either 'created' (when the star was
            created) or 'updated' (when the repository was last pushed to)
        :param str direction:
            (optional), either 'asc' or 'desc'. Default: 'desc'
        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository>`
        """
        params = {'sort': sort, 'direction': direction}
        self._remove_none(params)
        url = self._build_url('user', 'starred')
        return self._iter(int(number), url, repo.ShortRepository, params,
                          etag)

    def starred_by(self, username, sort=None, direction=None, number=-1,
                   etag=None):
        """Iterate over repositories starred by ``username``.

        .. versionadded:: 1.0

           This was split from ``iter_starred`` and requires the login
           parameter.

        :param str username:
            name of user whose stars you want to see
        :param str sort:
            (optional), either 'created' (when the star was created) or
            'updated' (when the repository was last pushed to)
        :param str direction:
            (optional), either 'asc' or 'desc'. Default: 'desc'
        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        params = {'sort': sort, 'direction': direction}
        self._remove_none(params)
        url = self._build_url('users', str(username), 'starred')
        return self._iter(int(number), url, repo.ShortRepository, params,
                          etag)

    @requires_auth
    def subscriptions(self, number=-1, etag=None):
        """Iterate over repositories subscribed to by the authenticated user.

        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        url = self._build_url('user', 'subscriptions')
        return self._iter(int(number), url, repo.ShortRepository, etag=etag)

    def subscriptions_for(self, username, number=-1, etag=None):
        """Iterate over repositories subscribed to by ``username``.

        :param str username:
            name of user whose subscriptions you want to see
        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of subscribed repositories
        :rtype:
            :class:`~github3.repos.repo.ShortRepository`
        """
        url = self._build_url('users', str(username), 'subscriptions')
        return self._iter(int(number), url, repo.ShortRepository, etag=etag)

    @requires_auth
    def unfollow(self, username):
        """Make the authenticated user stop following username.

        :param str username:
            (required)
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = False
        if username:
            url = self._build_url('user', 'following', username)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def unstar(self, username, repo):
        """Unstar username/repo.

        :param str username:
            (required), owner of the repo
        :param str repo:
            (required), name of the repo
        :return:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = False
        if username and repo:
            url = self._build_url('user', 'starred', username, repo)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def update_me(self, name=None, email=None, blog=None, company=None,
                  location=None, hireable=False, bio=None):
        """Update the profile of the authenticated user.

        :param str name:
            e.g., 'John Smith', not login name
        :param str email:
            e.g., 'john.smith@example.com'
        :param str blog:
            e.g., 'http://www.example.com/jsmith/blog'
        :param str company:
        :param str location:
        :param bool hireable:
            defaults to False
        :param str bio:
            GitHub flavored markdown
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        user = {'name': name, 'email': email, 'blog': blog,
                'company': company, 'location': location,
                'hireable': hireable, 'bio': bio}
        self._remove_none(user)
        url = self._build_url('user')
        _json = self._json(self._patch(url, data=json.dumps(user)), 200)
        if _json:
            self._update_attributes(_json)
            return True
        return False

    def user(self, username):
        """Retrieve a User object for the specified user name.

        :param str username:
            name of the user
        :returns:
            the user
        :rtype:
            :class:`~github3.users.User`
        """
        url = self._build_url('users', username)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(users.User, json)

    @requires_auth
    def user_issues(self, filter='', state='', labels='', sort='',
                    direction='', since=None, per_page=None, number=-1,
                    etag=None):
        """List only the authenticated user's issues.

        Will not list organization's issues. See :meth:`organization_issues`.

        .. versionchanged:: 1.0

            ``per_page`` parameter added before ``number``

        .. versionchanged:: 0.9.0

            - The ``state`` parameter now accepts 'all' in addition to 'open'
              and 'closed'.

        :param str filter:
            accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state:
            accepted values: ('all', 'open', 'closed')
            api-default: 'open'
        :param str labels:
            comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort:
            accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction:
            accepted values: ('asc', 'desc')
            api-default: desc
        :param since:
            (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since:
            :class:`~datetime.datetime` or str
        :param int number:
            (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag:
            (optional), ETag from a previous request to the same
            endpoint
        :returns:
            generator of issues
        :rtype:
            :class:`~github3.issues.ShortIssue`
        """
        url = self._build_url('user', 'issues')
        # issue_params will handle the since parameter
        params = issues.issue_params(
            filter, state, labels, sort, direction, since
        )
        params.update(per_page=per_page)
        return self._iter(int(number), url, issues.ShortIssue, params, etag)

    @requires_auth
    def user_teams(self, number=-1, etag=None):
        """Get the authenticated user's teams across all of organizations.

        List all of the teams across all of the organizations to which the
        authenticated user belongs. This method requires user or repo scope
        when authenticating via OAuth.

        :returns:
            generator of teams
        :rtype:
            :class:`~github3.orgs.ShortTeam`
        """
        url = self._build_url('user', 'teams')
        return self._iter(int(number), url, orgs.ShortTeam, etag=etag)

    def user_with_id(self, number):
        """Get the user's information with id ``number``.

        :param int number:
            the user's id number
        :returns:
            the user
        :rtype:
            :class:`~github3.users.User`
        """
        number = int(number)
        json = None
        if number > 0:
            url = self._build_url('user', str(number))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(users.User, json)

    def zen(self):
        """Return a quote from the Zen of GitHub.

        Yet another API Easter Egg

        :returns:
            the zen of GitHub
        :rtype:
            str (on Python 3, unicode on Python 2)
        """
        url = self._build_url('zen')
        resp = self._get(url)
        return resp.text if resp.status_code == 200 else b''.decode('utf-8')


class GitHubEnterprise(GitHub):
    """An interface to a specific GitHubEnterprise instance.

    For GitHub Enterprise users, this object will act as the public API to
    your instance. You must provide the URL to your instance upon
    initialization and can provide the rest of the login details just like in
    the :class:`GitHub <GitHub>` object.

    There is no need to provide the end of the url (e.g., /api/v3/), that will
    be taken care of by us.

    If you have a self signed SSL for your local github enterprise you can
    override the validation by passing `verify=False`.
    """

    def __init__(self, url, username='', password='', token='', verify=True):
        """Create a client for a GitHub Enterprise instance."""
        super(GitHubEnterprise, self).__init__(username, password, token)
        self.session.base_url = url.rstrip('/') + '/api/v3'
        self.session.verify = verify
        self.url = url

    def _repr(self):
        return '<GitHub Enterprise [{0.url}]>'.format(self)

    @requires_auth
    def create_user(self, login, email):
        """Create a new user.

        .. note::

            This is only available for administrators of the instance.

        :param str login:
            (required), The user's username.
        :param str email:
            (required), The user's email address.
        :returns:
            created user
        :rtype:
            :class:`ShortUser <github3.users.ShortUser>`
        """
        url = self._build_url('admin', 'users')
        payload = {'login': login, 'email': email}
        json_data = self._json(self._post(url, data=payload), 201)
        return self._instance_or_null(users.ShortUser, json_data)

    @requires_auth
    def admin_stats(self, option):
        """Retrieve statistics about this GitHub Enterprise instance.

        :param str option:
            (required), accepted values: ('all', 'repos',
            'hooks', 'pages', 'orgs', 'users', 'pulls', 'issues',
            'milestones', 'gists', 'comments')
        :returns:
            the statistics
        :rtype:
            dict
        """
        stats = {}
        if option.lower() in ('all', 'repos', 'hooks', 'pages', 'orgs',
                              'users', 'pulls', 'issues', 'milestones',
                              'gists', 'comments'):
            url = self._build_url('enterprise', 'stats', option.lower())
            stats = self._json(self._get(url), 200)
        return stats


class GitHubStatus(models.GitHubCore):
    """A sleek interface to the GitHub System Status API.

    This will only ever return the JSON objects returned by the API.
    """

    def __init__(self):
        """Create a status API client."""
        super(GitHubStatus, self).__init__({}, self.new_session())
        self.session.base_url = 'https://status.github.com'

    def _repr(self):
        return '<GitHub Status>'

    def _recipe(self, *args):
        url = self._build_url(*args)
        resp = self._get(url)
        return resp.json() if self._boolean(resp, 200, 404) else {}

    def api(self):
        """Retrieve API status."""
        return self._recipe('api.json')

    def status(self):
        """Retrieve overall status."""
        return self._recipe('api', 'status.json')

    def last_message(self):
        """Retrieve the last message."""
        return self._recipe('api', 'last-message.json')

    def messages(self):
        """Retrieve all messages."""
        return self._recipe('api', 'messages.json')
