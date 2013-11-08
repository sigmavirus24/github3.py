"""
github3.github
==============

This module contains the main GitHub session object.

"""

from json import dumps
from requests import session
from github3.auths import Authorization
from github3.events import Event
from github3.gists import Gist
from github3.issues import Issue, issue_params
from github3.legacy import LegacyIssue, LegacyRepo, LegacyUser
from github3.models import GitHubCore
from github3.orgs import Organization
from github3.repos import Repository
from github3.users import User, Key
from github3.decorators import requires_auth, requires_basic_auth
from github3.notifications import Thread


class GitHub(GitHubCore):
    """Stores all the session information.

    There are two ways to log into the GitHub API

    ::

        from github3 import login
        g = login(user, password)
        g = login(token=token)
        g = login(user, token=token)

    or

    ::

        from github3 import GitHub
        g = GitHub(user, password)
        g = GitHub(token=token)
        g = GitHub(user, token=token)

    This is simple backward compatibility since originally there was no way to
    call the GitHub object with authentication parameters.
    """
    def __init__(self, login='', password='', token=''):
        super(GitHub, self).__init__({})
        if token:
            self.login(login, token=token)
        elif login and password:
            self.login(login, password)

    def __repr__(self):
        if self._session.auth:
            return '<GitHub [{0[0]}]>'.format(self._session.auth)
        return '<GitHub at 0x{0:x}>'.format(id(self))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @requires_auth
    def _iter_follow(self, which, number, etag):
        url = self._build_url('user', which)
        return self._iter(number, url, User, etag=etag)

    @requires_basic_auth
    def authorization(self, id_num):
        """Get information about authorization ``id``.

        :param int id_num: (required), unique id of the authorization
        :returns: :class:`Authorization <Authorization>`
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('authorizations', str(id_num))
            json = self._json(self._get(url), 200)
        return Authorization(json, self) if json else None

    def authorize(self, login, password, scopes=None, note='', note_url='',
                  client_id='', client_secret=''):
        """Obtain an authorization token from the GitHub API for the GitHub
        API.

        :param str login: (required)
        :param str password: (required)
        :param list scopes: (optional), areas you want this token to apply to,
            i.e., 'gist', 'user'
        :param str note: (optional), note about the authorization
        :param str note_url: (optional), url for the application
        :param str client_id: (optional), 20 character OAuth client key for
            which to create a token
        :param str client_secret: (optional), 40 character OAuth client secret
            for which to create the token
        :returns: :class:`Authorization <Authorization>`
        """
        json = None
        auth = self._session.auth or (login and password)
        if auth:
            url = self._build_url('authorizations')
            data = {'note': note, 'note_url': note_url,
                    'client_id': client_id, 'client_secret': client_secret}
            if scopes:
                data['scopes'] = scopes
            if self._session.auth:
                json = self._json(self._post(url, data=data), 201)
            else:
                ses = session()
                ses.auth = (login, password)
                json = self._json(ses.post(url, data=dumps(data)), 201)
        return Authorization(json, self) if json else None

    def check_authorization(self, access_token):
        """OAuth applications can use this method to check token validity
        without hitting normal rate limits because of failed login attempts.
        If the token is valid, it will return True, otherwise it will return
        False.

        :returns: bool
        """
        p = self._session.params
        auth = (p.get('client_id'), p.get('client_secret'))
        if access_token and auth:
            url = self._build_url('applications', str(auth[0]), 'tokens',
                                  str(access_token))
            resp = self._get(url, auth=auth, params={
                'client_id': None, 'client_secret': None
            })
            return self._boolean(resp, 200, 404)
        return False

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.

        :param str description: (required), description of gist
        :param dict files: (required), file names with associated dictionaries
            for content, e.g. ``{'spam.txt': {'content': 'File contents
            ...'}}``
        :param bool public: (optional), make the gist public if True
        :returns: :class:`Gist <github3.gists.Gist>`
        """
        new_gist = {'description': description, 'public': public,
                    'files': files}
        url = self._build_url('gists')
        json = self._json(self._post(url, data=new_gist), 201)
        return Gist(json, self) if json else None

    @requires_auth
    def create_issue(self,
                     owner,
                     repository,
                     title,
                     body=None,
                     assignee=None,
                     milestone=None,
                     labels=[]):
        """Create an issue on the project 'repository' owned by 'owner'
        with title 'title'.

        body, assignee, milestone, labels are all optional.

        :param str owner: (required), login of the owner
        :param str repository: (required), repository name
        :param str title: (required), Title of issue to be created
        :param str body: (optional), The text of the issue, markdown
            formatted
        :param str assignee: (optional), Login of person to assign
            the issue to
        :param str milestone: (optional), Which milestone to assign
            the issue to
        :param list labels: (optional), List of label names.
        :returns: :class:`Issue <github3.issues.Issue>`
        """
        repo = None
        if owner and repository and title:
            repo = self.repository(owner, repository)

        if repo:
            return repo.create_issue(title, body, assignee, milestone, labels)

        # Regardless, something went wrong. We were unable to create the
        # issue
        return None

    @requires_auth
    def create_key(self, title, key):
        """Create a new key for the authenticated user.

        :param str title: (required), key title
        :param key: (required), actual key contents, accepts path as a string
            or file-like object
        :returns: :class:`Key <github3.users.Key>`
        """
        created = None

        if title and key:
            url = self._build_url('user', 'keys')
            req = self._post(url, data={'title': title, 'key': key})
            json = self._json(req, 201)
            if json:
                created = Key(json, self)
        return created

    @requires_auth
    def create_repo(self,
                    name,
                    description='',
                    homepage='',
                    private=False,
                    has_issues=True,
                    has_wiki=True,
                    has_downloads=True,
                    auto_init=False,
                    gitignore_template=''):
        """Create a repository for the authenticated user.

        :param str name: (required), name of the repository
        :param str description: (optional)
        :param str homepage: (optional)
        :param str private: (optional), If ``True``, create a
            private repository. API default: ``False``
        :param bool has_issues: (optional), If ``True``, enable
            issues for this repository. API default: ``True``
        :param bool has_wiki: (optional), If ``True``, enable the
            wiki for this repository. API default: ``True``
        :param bool has_downloads: (optional), If ``True``, enable
            downloads for this repository. API default: ``True``
        :param bool auto_init: (optional), auto initialize the repository
        :param str gitignore_template: (optional), name of the git template to
            use; ignored if auto_init = False.
        :returns: :class:`Repository <github3.repos.Repository>`

        .. warning: ``name`` should be no longer than 100 characters
        """
        url = self._build_url('user', 'repos')
        data = {'name': name, 'description': description,
                'homepage': homepage, 'private': private,
                'has_issues': has_issues, 'has_wiki': has_wiki,
                'has_downloads': has_downloads, 'auto_init': auto_init,
                'gitignore_template': gitignore_template}
        json = self._json(self._post(url, data=data), 201)
        return Repository(json, self) if json else None

    @requires_auth
    def delete_key(self, key_id):
        """Delete user key pointed to by ``key_id``.

        :param int key_id: (required), unique id used by Github
        :returns: bool
        """
        key = self.key(key_id)
        if key:
            return key.delete()
        return False  # (No coverage)

    @requires_auth
    def follow(self, login):
        """Make the authenticated user follow login.

        :param str login: (required), user to follow
        :returns: bool
        """
        resp = False
        if login:
            url = self._build_url('user', 'following', login)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    def gist(self, id_num):
        """Gets the gist using the specified id number.

        :param int id_num: (required), unique id of the gist
        :returns: :class:`Gist <github3.gists.Gist>`
        """
        url = self._build_url('gists', str(id_num))
        json = self._json(self._get(url), 200)
        return Gist(json, self) if json else None

    def gitignore_template(self, language):
        """Returns the template for language.

        :returns: str
        """
        url = self._build_url('gitignore', 'templates', language)
        json = self._json(self._get(url), 200)
        return json.get('source', '')

    def gitignore_templates(self):
        """Returns the list of available templates.

        :returns: list of template names
        """
        url = self._build_url('gitignore', 'templates')
        return self._json(self._get(url), 200) or []

    @requires_auth
    def is_following(self, login):
        """Check if the authenticated user is following login.

        :param str login: (required), login of the user to check if the
            authenticated user is checking
        :returns: bool
        """
        json = False
        if login:
            url = self._build_url('user', 'following', login)
            json = self._boolean(self._get(url), 204, 404)
        return json

    @requires_auth
    def is_starred(self, login, repo):
        """Check if the authenticated user starred login/repo.

        :param str login: (required), owner of repository
        :param str repo: (required), name of repository
        :returns: bool
        """
        json = False
        if login and repo:
            url = self._build_url('user', 'starred', login, repo)
            json = self._boolean(self._get(url), 204, 404)
        return json

    @requires_auth
    def is_subscribed(self, login, repo):
        """Check if the authenticated user is subscribed to login/repo.

        :param str login: (required), owner of repository
        :param str repo: (required), name of repository
        :returns: bool
        """
        json = False
        if login and repo:
            url = self._build_url('user', 'subscriptions', login, repo)
            json = self._boolean(self._get(url), 204, 404)
        return json

    def issue(self, owner, repository, number):
        """Fetch issue #:number: from https://github.com/:owner:/:repository:

        :param str owner: (required), owner of the repository
        :param str repository: (required), name of the repository
        :param int number: (required), issue number
        :return: :class:`Issue <github3.issues.Issue>`
        """
        repo = self.repository(owner, repository)
        if repo:
            return repo.issue(number)
        return None

    def iter_all_repos(self, number=-1, since=None, etag=None, per_page=None):
        """Iterate over every repository in the order they were created.

        :param int number: (optional), number of repositories to return.
            Default: -1, returns all of them
        :param int since: (optional), last repository id seen (allows
            restarting this iteration)
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :param int per_page: (optional), number of repositories to list per
            request
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        url = self._build_url('repositories')
        return self._iter(int(number), url, Repository,
                          params={'since': since, 'per_page': per_page},
                          etag=etag)

    def iter_all_users(self, number=-1, etag=None, per_page=None):
        """Iterate over every user in the order they signed up for GitHub.

        :param int number: (optional), number of users to return. Default: -1,
            returns all of them
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :param int per_page: (optional), number of users to list per request
        :returns: generator of :class:`User <github3.users.User>`
        """
        url = self._build_url('users')
        return self._iter(int(number), url, User,
                          params={'per_page': per_page}, etag=etag)

    @requires_basic_auth
    def iter_authorizations(self, number=-1, etag=None):
        """Iterate over authorizations for the authenticated user. This will
        return a 404 if you are using a token for authentication.

        :param int number: (optional), number of authorizations to return.
            Default: -1 returns all available authorizations
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Authorization <Authorization>`\ s
        """
        url = self._build_url('authorizations')
        return self._iter(int(number), url, Authorization, etag=etag)

    @requires_auth
    def iter_emails(self, number=-1, etag=None):
        """Iterate over email addresses for the authenticated user.

        :param int number: (optional), number of email addresses to return.
            Default: -1 returns all available email addresses
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of dicts
        """
        url = self._build_url('user', 'emails')
        return self._iter(int(number), url, dict, etag=etag)

    def iter_events(self, number=-1, etag=None):
        """Iterate over public events.

        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        url = self._build_url('events')
        return self._iter(int(number), url, Event, etag=etag)

    def iter_followers(self, login=None, number=-1, etag=None):
        """If login is provided, iterate over a generator of followers of that
        login name; otherwise return a generator of followers of the
        authenticated user.

        :param str login: (optional), login of the user to check
        :param int number: (optional), number of followers to return. Default:
            -1 returns all followers
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        if login:
            return self.user(login).iter_followers()
        return self._iter_follow('followers', int(number), etag=etag)

    def iter_following(self, login=None, number=-1, etag=None):
        """If login is provided, iterate over a generator of users being
        followed by login; otherwise return a generator of people followed by
        the authenticated user.

        :param str login: (optional), login of the user to check
        :param int number: (optional), number of people to return. Default: -1
            returns all people you follow
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        if login:
            return self.user(login).iter_following()
        return self._iter_follow('following', int(number), etag=etag)

    def iter_gists(self, username=None, number=-1, etag=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists

        :param str login: (optional), login of the user to check
        :param int number: (optional), number of gists to return. Default: -1
            returns all available gists
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Gist <github3.gists.Gist>`\ s
        """
        if username:
            url = self._build_url('users', username, 'gists')
        else:
            url = self._build_url('gists')
        return self._iter(int(number), url, Gist, etag=etag)

    @requires_auth
    def iter_notifications(self, all=False, participating=False, number=-1,
                           etag=None):
        """Iterate over the user's notification.

        :param bool all: (optional), iterate over all notifications
        :param bool participating: (optional), only iterate over notifications
            in which the user is participating
        :param int number: (optional), how many notifications to return
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of
            :class:`Thread <github3.notifications.Thread>`
        """
        params = None
        if all:
            params = {'all': all}
        elif participating:
            params = {'participating': participating}

        url = self._build_url('notifications')
        return self._iter(int(number), url, Thread, params, etag=etag)

    @requires_auth
    def iter_org_issues(self, name, filter='', state='', labels='', sort='',
                        direction='', since=None, number=-1, etag=None):
        """Iterate over the organnization's issues if the authenticated user
        belongs to it.

        :param str name: (required), name of the organization
        :param str filter: accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state: accepted values: ('open', 'closed')
            api-default: 'open'
        :param str labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction: accepted values: ('asc', 'desc')
            api-default: desc
        :param since: (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since: datetime or string
        :param int number: (optional), number of issues to return. Default:
            -1, returns all available issues
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Issue <github3.issues.Issue>`
        """
        url = self._build_url('orgs', name, 'issues')
        # issue_params will handle the since parameter
        params = issue_params(filter, state, labels, sort, direction, since)
        return self._iter(int(number), url, Issue, params, etag)

    @requires_auth
    def iter_issues(self, filter='', state='', labels='', sort='',
                    direction='', since=None, number=-1, etag=None):
        """List all of the authenticated user's (and organization's) issues.

        :param str filter: accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state: accepted values: ('open', 'closed')
            api-default: 'open'
        :param str labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction: accepted values: ('asc', 'desc')
            api-default: desc
        :param since: (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since: datetime or string
        :param int number: (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Issue <github3.issues.Issue>`
        """
        url = self._build_url('issues')
        # issue_params will handle the since parameter
        params = issue_params(filter, state, labels, sort, direction, since)
        return self._iter(int(number), url, Issue, params, etag)

    @requires_auth
    def iter_user_issues(self, filter='', state='', labels='', sort='',
                         direction='', since=None, number=-1, etag=None):
        """List only the authenticated user's issues. Will not list
        organization's issues

        :param str filter: accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :param str state: accepted values: ('open', 'closed')
            api-default: 'open'
        :param str labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction: accepted values: ('asc', 'desc')
            api-default: desc
        :param since: (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since: datetime or string
        :param int number: (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Issue <github3.issues.Issue>`
        """
        url = self._build_url('user', 'issues')
        # issue_params will handle the since parameter
        params = issue_params(filter, state, labels, sort, direction, since)
        return self._iter(int(number), url, Issue, params, etag)

    def iter_repo_issues(self, owner, repository, milestone=None,
                         state=None, assignee=None, mentioned=None,
                         labels=None, sort=None, direction=None, since=None,
                         number=-1, etag=None):
        """List issues on owner/repository. Only owner and repository are
        required.

        :param str owner: login of the owner of the repository
        :param str repository: name of the repository
        :param int milestone: None, '*', or ID of milestone
        :param str state: accepted values: ('open', 'closed')
            api-default: 'open'
        :param str assignee: '*' or login of the user
        :param str mentioned: login of the user
        :param str labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param str sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param str direction: accepted values: ('asc', 'desc')
            api-default: desc
        :param since: (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since: datetime or string
        :param int number: (optional), number of issues to return.
            Default: -1 returns all issues
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Issue <github3.issues.Issue>`\ s
        """
        if owner and repository:
            repo = self.repository(owner, repository)
            return repo.iter_issues(milestone, state, assignee, mentioned,
                                    labels, sort, direction, since, number,
                                    etag)
        return iter([])

    @requires_auth
    def iter_keys(self, number=-1, etag=None):
        """Iterate over public keys for the authenticated user.

        :param int number: (optional), number of keys to return. Default: -1
            returns all your keys
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Key <github3.users.Key>`\ s
        """
        url = self._build_url('user', 'keys')
        return self._iter(int(number), url, Key, etag=etag)

    def iter_orgs(self, login=None, number=-1, etag=None):
        """Iterate over public organizations for login if provided; otherwise
        iterate over public and private organizations for the authenticated
        user.

        :param str login: (optional), user whose orgs you wish to list
        :param int number: (optional), number of organizations to return.
            Default: -1 returns all available organizations
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of
            :class:`Organization <github3.orgs.Organization>`\ s
        """
        if login:
            url = self._build_url('users', login, 'orgs')
        else:
            url = self._build_url('user', 'orgs')

        return self._iter(int(number), url, Organization, etag=etag)

    @requires_auth
    def iter_repos(self, type=None, sort=None, direction=None, number=-1,
                   etag=None):
        """List public repositories for the authenticated user.

        .. versionchanged:: 0.6
           Removed the login parameter for correctness. Use iter_user_repos
           instead

        :param str type: (optional), accepted values:
            ('all', 'owner', 'public', 'private', 'member')
            API default: 'all'
        :param str sort: (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :param str direction: (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :param int number: (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
            objects
        """
        url = self._build_url('user', 'repos')

        params = {}
        if type in ('all', 'owner', 'public', 'private', 'member'):
            params.update(type=type)
        if sort in ('created', 'updated', 'pushed', 'full_name'):
            params.update(sort=sort)
        if direction in ('asc', 'desc'):
            params.update(direction=direction)

        return self._iter(int(number), url, Repository, params, etag)

    def iter_starred(self, login=None, sort=None, direction=None, number=-1,
                     etag=None):
        """Iterate over repositories starred by ``login`` or the authenticated
        user.

        .. versionchanged:: 0.5
           Added sort and direction parameters (optional) as per the change in
           GitHub's API.

        :param str login: (optional), name of user whose stars you want to see
        :param str sort: (optional), either 'created' (when the star was
            created) or 'updated' (when the repository was last pushed to)
        :param str direction: (optional), either 'asc' or 'desc'. Default:
            'desc'
        :param int number: (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        if login:
            return self.user(login).iter_starred(sort, direction)

        params = {'sort': sort, 'direction': direction}
        self._remove_none(params)
        url = self._build_url('user', 'starred')
        return self._iter(int(number), url, Repository, params, etag)

    def iter_subscriptions(self, login=None, number=-1, etag=None):
        """Iterate over repositories subscribed to by ``login`` or the
        authenticated user.

        :param str login: (optional), name of user whose subscriptions you want
            to see
        :param int number: (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        if login:
            return self.user(login).iter_subscriptions()

        url = self._build_url('user', 'subscriptions')
        return self._iter(int(number), url, Repository, etag=etag)

    def iter_user_repos(self, login, type=None, sort=None, direction=None,
                        number=-1, etag=None):
        """List public repositories for the specified ``login``.

        .. versionadded:: 0.6

        :param str login: (required), username
        :param str type: (optional), accepted values:
            ('all', 'owner', 'member')
            API default: 'all'
        :param str sort: (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :param str direction: (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :param int number: (optional), number of repositories to return.
            Default: -1 returns all repositories
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
            objects
        """
        url = self._build_url('users', login, 'repos')

        params = {}
        if type in ('all', 'owner', 'member'):
            params.update(type=type)
        if sort in ('created', 'updated', 'pushed', 'full_name'):
            params.update(sort=sort)
        if direction in ('asc', 'desc'):
            params.update(direction=direction)

        return self._iter(int(number), url, Repository, params, etag)

    @requires_auth
    def key(self, id_num):
        """Gets the authenticated user's key specified by id_num.

        :param int id_num: (required), unique id of the key
        :returns: :class:`Key <github3.users.Key>`
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('user', 'keys', str(id_num))
            json = self._json(self._get(url), 200)
        return Key(json, self) if json else None

    def login(self, username=None, password=None, token=None):
        """Logs the user into GitHub for protected API calls.

        :param str username: (optional)
        :param str password: (optional)
        :param str token: (optional)
        """
        if username and password:
            self._session.auth = (username, password)
        elif token:
            self._session.headers.update({
                'Authorization': 'token ' + token})

    def markdown(self, text, mode='', context='', raw=False):
        """Render an arbitrary markdown document.

        :param str text: (required), the text of the document to render
        :param str mode: (optional), 'markdown' or 'gfm'
        :param str context: (optional), only important when using mode 'gfm',
            this is the repository to use as the context for the rendering
        :param bool raw: (optional), renders a document like a README.md, no
            gfm, no context
        :returns: str -- HTML formatted text
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

        if data:
            req = self._post(url, data=data, json=json, headers=headers)
            if req.ok:
                return req.content
        return ''  # (No coverage)

    def meta(self):
        """Returns an array of addresses in CIDR format specifying the
        addresses that the incoming service hooks will originate from.

        .. versionadded:: 0.5
        """
        url = self._build_url('meta')
        return self._json(self._get(url), 200)

    def octocat(self, say=None):
        """Returns an easter egg of the API.

        :params str say: (optional), pass in what you'd like Octocat to say
        :returns: ascii art of Octocat
        """
        url = self._build_url('octocat')
        req = self._get(url, params={'s': say})
        return req.content if req.ok else ''

    def organization(self, login):
        """Returns a Organization object for the login name

        :param str login: (required), login name of the org
        :returns: :class:`Organization <github3.orgs.Organization>`
        """
        url = self._build_url('orgs', login)
        json = self._json(self._get(url), 200)
        return Organization(json, self) if json else None

    @requires_auth
    def pubsubhubbub(self, mode, topic, callback, secret=''):
        """Create/update a pubsubhubbub hook.

        :param str mode: (required), accepted values: ('subscribe',
            'unsubscribe')
        :param str topic: (required), form:
            https://github.com/:user/:repo/events/:event
        :param str callback: (required), the URI that receives the updates
        :param str secret: (optional), shared secret key that generates a
            SHA1 HMAC of the payload content.
        :returns: bool
        """
        from re import match
        m = match('https://[\w\d\-\.\:]+/\w+/[\w\._-]+/events/\w+', topic)
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
            status = self._boolean(self._post(url, data=data, json=False), 204,
                                   404)
        return status

    def pull_request(self, owner, repository, number):
        """Fetch pull_request #:number: from :owner:/:repository

        :param str owner: (required), owner of the repository
        :param str repository: (required), name of the repository
        :param int number: (required), issue number
        :return: :class:`Issue <github3.issues.Issue>`
        """
        r = self.repository(owner, repository)
        return r.pull_request(number) if r else None

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of
        owner and repository

        :param str owner: (required)
        :param str repository: (required)
        :returns: :class:`Repository <github3.repos.Repository>`
        """
        json = None
        if owner and repository:
            url = self._build_url('repos', owner, repository)
            json = self._json(self._get(url), 200)
        return Repository(json, self) if json else None

    def search_issues(self, owner, repo, state, keyword, start_page=0):
        """Find issues by state and keyword.

        :param str owner: (required)
        :param str repo: (required)
        :param str state: (required), accepted values: ('open', 'closed')
        :param str keyword: (required), what to search for
        :param int start_page: (optional), page to get (results come 100/page)
        :returns: list of :class:`LegacyIssue <github3.legacy.LegacyIssue>`\ s
        """
        params = {'start_page': int(start_page)} if int(start_page) > 0 else {}
        url = self._build_url('legacy', 'issues', 'search', owner, repo,
                              state, keyword)
        json = self._json(self._get(url, params=params), 200)
        issues = json.get('issues', [])
        return [LegacyIssue(l, self) for l in issues]

    def search_repos(self, keyword, language=None, start_page=None,
                     sort=None, order=None):
        """Search all repositories by keyword.

        :param str keyword: (required)
        :param str language: (optional), language to filter by
        :param int start_page: (optional), page to get (results come 100/page)
        :param str sort: (optional), how to sort the results; accepted values:
            ('stars', 'forks', 'updated')
        :param str order: (optional), sort order if ``sort`` isn't provided,
            accepted values: ('asc', 'desc')
        :returns: list of :class:`LegacyRepo <github3.legacy.LegacyRepo>`\ s
        """
        url = self._build_url('legacy', 'repos', 'search', keyword)
        params = {'language': language, 'start_page': start_page}
        if sort in ('stars', 'forks', 'updated'):
            params['sort'] = sort
        if order in ('asc', 'desc') and not sort:
            params['order'] = order
        json = self._json(self._get(url, params=params), 200)
        repos = json.get('repositories', [])
        return [LegacyRepo(r, self) for r in repos]

    def search_users(self, keyword, start_page=0, sort=None, order=None):
        """Search all users by keyword.

        :param str keyword: (required)
        :param int start_page: (optional), page to get (results come 100/page)
        :param str sort: (optional), how to sort the results; accepted values:
            ('followers', 'joined', 'repositories')
        :param str order: (optional), sort order if ``sort`` isn't provided,
            accepted values: ('asc', 'desc')
        :returns: list of :class:`LegacyUser <github3.legacy.LegacyUser>`\ s
        """
        params = {'start_page': int(start_page)} if int(start_page) > 0 else {}
        if sort in ('followers', 'joined', 'repositories'):
            params['sort'] = sort
        if order in ('asc', 'desc') and not sort:
            params['order'] = order
        url = self._build_url('legacy', 'user', 'search', str(keyword))
        json = self._json(self._get(url, params=params), 200)
        users = json.get('users', [])
        return [LegacyUser(u, self) for u in users]

    def search_email(self, email):
        """Search users by email.

        :param str email: (required)
        :returns: :class:`LegacyUser <github3.legacy.LegacyUser>`
        """
        url = self._build_url('legacy', 'user', 'email', email)
        json = self._json(self._get(url), 200)
        u = json.get('user', {})
        return LegacyUser(u, self) if u else None

    def set_client_id(self, id, secret):
        """Allows the developer to set their client_id and client_secret for
        their OAuth application.

        :param str id: 20-character hexidecimal client_id provided by GitHub
        :param str secret: 40-character hexidecimal client_secret provided by
            GitHub
        """
        self._session.params = {'client_id': id, 'client_secret': secret}

    def set_user_agent(self, user_agent):
        """Allows the user to set their own user agent string to identify with
        the API.

        :param str user_agent: String used to identify your application.
            Library default: "github3.py/{version}", e.g., "github3.py/0.5"
        """
        if not user_agent:
            return
        self._session.headers.update({'User-Agent': user_agent})

    @requires_auth
    def star(self, login, repo):
        """Star to login/repo

        :param str login: (required), owner of the repo
        :param str repo: (required), name of the repo
        :return: bool
        """
        resp = False
        if login and repo:
            url = self._build_url('user', 'starred', login, repo)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    @requires_auth
    def subscribe(self, login, repo):
        """Subscribe to login/repo

        :param str login: (required), owner of the repo
        :param str repo: (required), name of the repo
        :return: bool
        """
        resp = False
        if login and repo:
            url = self._build_url('user', 'subscriptions', login, repo)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    @requires_auth
    def unfollow(self, login):
        """Make the authenticated user stop following login

        :param str login: (required)
        :returns: bool
        """
        resp = False
        if login:
            url = self._build_url('user', 'following', login)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def unstar(self, login, repo):
        """Unstar to login/repo

        :param str login: (required), owner of the repo
        :param str repo: (required), name of the repo
        :return: bool
        """
        resp = False
        if login and repo:
            url = self._build_url('user', 'starred', login, repo)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def unsubscribe(self, login, repo):
        """Unsubscribe to login/repo

        :param str login: (required), owner of the repo
        :param str repo: (required), name of the repo
        :return: bool
        """
        resp = False
        if login and repo:
            url = self._build_url('user', 'subscriptions', login, repo)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def update_user(self, name=None, email=None, blog=None,
                    company=None, location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters. All parameters are
        optional.

        :param str name: e.g., 'John Smith', not login name
        :param str email: e.g., 'john.smith@example.com'
        :param str blog: e.g., 'http://www.example.com/jsmith/blog'
        :param str company: company name
        :param str location: where you are located
        :param bool hireable: defaults to False
        :param str bio: GitHub flavored markdown
        :returns: bool
        """
        user = self.user()
        return user.update(name, email, blog, company, location, hireable,
                           bio)

    def user(self, login=None):
        """Returns a User object for the specified login name if
        provided. If no login name is provided, this will return a User
        object for the authenticated user.

        :param str login: (optional)
        :returns: :class:`User <github3.users.User>`
        """
        if login:
            url = self._build_url('users', login)
        else:
            url = self._build_url('user')

        json = self._json(self._get(url), 200)
        return User(json, self._session) if json else None

    def zen(self):
        """Returns a quote from the Zen of GitHub. Yet another API Easter Egg

        :returns: str
        """
        url = self._build_url('zen')
        resp = self._get(url)
        return resp.content if resp.status_code == 200 else ''


class GitHubEnterprise(GitHub):
    """For GitHub Enterprise users, this object will act as the public API to
    your instance. You must provide the URL to your instance upon
    initializaiton and can provide the rest of the login details just like in
    the :class:`GitHub <GitHub>` object.

    There is no need to provide the end of the url (e.g., /api/v3/), that will
    be taken care of by us.
    """
    def __init__(self, url, login='', password='', token=''):
        super(GitHubEnterprise, self).__init__(login, password, token)
        self._github_url = url.rstrip('/') + '/api/v3'

    def __repr__(self):
        return '<GitHub Enterprise [0.url]>'.format(self)

    @requires_auth
    def admin_stats(self, option):
        """This is a simple way to get statistics about your system.

        :param str option: (required), accepted values: ('all', 'repos',
            'hooks', 'pages', 'orgs', 'users', 'pulls', 'issues',
            'milestones', 'gists', 'comments')
        :returns: dict
        """
        stats = {}
        if option.lower() in ('all', 'repos', 'hooks', 'pages', 'orgs',
                              'users', 'pulls', 'issues', 'milestones',
                              'gists', 'comments'):
            url = self._build_url('enterprise', 'stats', option.lower())
            stats = self._json(self._get(url), 200)
        return stats


class GitHubStatus(GitHubCore):
    """A sleek interface to the GitHub System Status API. This will only ever
    return the JSON objects returned by the API.
    """
    def __init__(self):
        super(GitHubStatus, self).__init__({})
        self._github_url = 'https://status.github.com'

    def __repr__(self):
        return '<GitHub Status>'

    def _recipe(self, *args):
        url = self._build_url(*args)
        resp = self._get(url)
        return resp.json() if self._boolean(resp, 200, 404) else {}

    def api(self):
        """GET /api.json"""
        return self._recipe('api.json')

    def status(self):
        """GET /api/status.json"""
        return self._recipe('api', 'status.json')

    def last_message(self):
        """GET /api/last-message.json"""
        return self._recipe('api', 'last-message.json')

    def messages(self):
        """GET /api/messages.json"""
        return self._recipe('api', 'messages.json')
