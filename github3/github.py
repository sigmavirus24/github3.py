"""
github3.github
==============

This module contains the main GitHub session object.

"""

from requests import session
from json import dumps
from .event import Event
from .gist import Gist
from .issue import Issue, issue_params
from .models import GitHubCore
from .org import Organization
from .repo import Repository
from .user import User, Key


class GitHub(GitHubCore):
    """Stores all the session information."""
    def __init__(self):
        super(GitHub, self).__init__()
        self._session = session()
        # Only accept JSON responses
        self._session.headers.update(
                {'Accept': 'application/vnd.github.full+json'})
        # Only accept UTF-8 encoded data
        self._session.headers.update({'Accept-Charset': 'utf-8'})
        # Identify who we are
        self._session.config['base_headers'].update(
                {'User-Agent': 'github3.py/pre-alpha'})

    def __repr__(self):
        return '<GitHub at 0x%x>' % id(self)

    def _list_follow(self, login, which):
        url = self._github_url + '/user/' + which
        json = self._get(url)
        return [User(f, self._session) for f in json]

    def authorize(self, login, password, scopes):
        """Obtain an authorization token from the GitHub API for the GitHub 
        API.
        
        :param login: (required)
        :type login: str
        :param password: (required)
        :type password: str
        :param scopes: (required), areas you want this token to apply to,
            i.e., 'gist', 'user'
        :type scopes: list of strings
        :returns: str (the token)
        """
        json = {}
        if isinstance(scopes, list) and scopes:
            url = 'https://api.github.com/authorizations'
            json = self._get(url, data={'scopes': scopes})
        return json.get('token', '')

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.

        :param description: (required), description of gist
        :type description: str
        :param files: (required), file names with associated dictionaries for
            content, e.g. ``{'spam.txt': {'content': 'File contents ...'}}``
        :type files: dict
        :param public: (optional), make the gist public if True
        :type public: bool
        :returns: :class:`Gist <github3.gist.Gist>`
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        url = self._github_url + '/gists'
        json = self._post(url, dumps(new_gist))
        return Gist(json, self._session) if json else None

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

        :param owner: (required), login of the owner
        :type owner: str
        :param repository: (required), repository name
        :type repository: str
        :param title: (required), Title of issue to be created
        :type title: str
        :param body: (optional), The text of the issue, markdown
            formatted
        :type body: str
        :param assignee: (optional), Login of person to assign
            the issue to
        :type assignee: str
        :param milestone: (optional), Which milestone to assign
            the issue to
        :type milestone: str
        :param labels: (optional), List of label names.
        :type labels: list
        :returns: :class:`Issue <github3.issue.Issue>`
        """
        repo = None
        if owner and repository and title:
            repo = self.repository(owner, repository)

        if repo:
            return repo.create_issue(title, body, assignee, milestone,
                    labels)

        # Regardless, something went wrong. We were unable to create the
        # issue
        return None

    def create_key(self, title, key):
        """Create a new key for the authenticated user.
        
        :param title: (required), key title
        :type title: str
        :param key: (required), actual key contents
        :type key: str or file
        :returns: :class:`Key <github3.user.Key>`
        """
        created = None

        if title and key:
            url = self._github_url + '/user/keys'
            json = self._post(url, {'title': title, 'key': key})
            if json:
                created = Key(resp.json, self._session)
        return created

    def create_repo(self,
        name,
        description='',
        homepage='',
        private=False,
        has_issues=True,
        has_wiki=True,
        has_downloads=True):
        """Create a repository for the authenticated user.

        :param name: (required), name of the repository
        :type name: str
        :param description: (optional)
        :type description: str
        :param homepage: (optional)
        :type homepage: str
        :param private: (optional), If ``True``, create a
            private repository. API default: ``False``
        :type private: bool
        :param has_issues: (optional), If ``True``, enable
            issues for this repository. API default: ``True``
        :type has_issues: bool
        :param has_wiki: (optional), If ``True``, enable the
            wiki for this repository. API default: ``True``
        :type has_wiki: bool
        :param has_downloads: (optional), If ``True``, enable
            downloads for this repository. API default: ``True``
        :type has_downloads: bool
        :returns: :class:`Repository <github3.repo.Repository>`
        """
        url = self._github_url + '/user/repos'
        data = dumps({'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads})
        json = self._post(url, data)
        return Repository(json, self._session) if json else None

    def delete_key(self, key_id):
        """Delete user key pointed to by ``key_id``.

        :param key_id: (required), unique id used by Github
        :type: int
        :returns: bool
        """
        key = self.get_key(key_id)
        if key:
            return key.delete()
        return False

    def follow(self, login):
        """Make the authenticated user follow login.
        
        :param login: (required), user to follow
        :type login: str
        :returns: bool
        """
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._put(url)
        return resp

    def get_key(self, id_num):
        """Gets the authenticated user's key specified by id_num.
        
        :param id_num: (required), unique id of the key
        :type id_num: int
        :returns: :class:`Key <github3.user.Key>`
        """
        json = None
        if int(id_num) > 0:
            url = '{0}/user/keys/{1}'.format(self._github_url,
                    str(id_num))
            json = self._get(url)
        return Key(json, self._session) if json else None

    def gist(self, id_num):
        """Gets the gist using the specified id number.
        
        :param id_num: (required), unique id of the gist
        :type id_num: int
        :returns: :class:`Gist <github3.gist.Gist>`
        """
        url = '{0}/gists/{1}'.format(self._github_url, str(id_num))
        json = self._get(url)
        return Gist(json, self._session) if json else None

    def is_following(self, login):
        """Check if the authenticated user is following login.
        
        :param login: (required), login of the user to check if the
            authenticated user is checking
        :type login: str
        :returns: bool
        """
        json = None
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url, login)
            json = self._session.get(url).status_code == 204
        return True if json else False

    def is_watching(self, login, repo):
        """Check if the authenticated user is following login/repo.
        
        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        json = None
        if login and repo:
            url = '/'.join([self._github_url, 'user/watched', login, repo])
            json = self._session.get(url).status_code == 204
        return True if json else False

    def issue(self, owner, repository, number):
        """Fetch issue #:number: from https://github.com/:owner:/:repository:
            
        :param owner: (required), owner of the repository
        :type owner: str
        :param repository: (required), name of the repository
        :type repository: str
        :param number: (required), issue number
        :type number: int
        :return: :class:`Issue <github3.issue.Issue>`
        """
        repo = self.repository(owner, repository)
        if repo:
            return repo.issue(number)
        return None

    def list_emails(self):
        """List email addresses for the authenticated user.
        
        :returns: list of dicts
        """
        url = self._github_url + '/user/emails'
        return self._get(url) or []

    def list_events(self):
        """List public events.
        
        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        json = self._get(self._github_url + '/events')
        return [Event(ev, self._session) for ev in json]

    def list_followers(self, login=None):
        """If login is provided, return a list of followers of that
        login name; otherwise return a list of followers of the
        authenticated user.
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        if login:
            return self.user(login).list_followers()
        return self._list_follow('followers')

    def list_following(self, login=None):
        """If login is provided, return a list of users being followed
        by login; otherwise return a list of people followed by the
        authenticated user.
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        if login:
            return self.user(login).list_following()
        return self._list_follow('following')

    def list_gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`Gist <github3.gist.Gist>`\ s
        """
        url = [self._github_url]
        if username:
            url.extend(['users', username, 'gists'])
        else:
            url.append('gists')
        url = '/'.join(url)

        json = self._get(url)
        ses = self._session
        return [Gist(gist, ses) for gist in json]

    def list_issues(self,
        owner=None,
        repository=None,
        filter=None,
        state=None,
        labels=None,
        sort=None,
        direction=None,
        since=None):
        """If no parameters are provided, this gets the issues for the
        authenticated user. All parameters are optional with the
        exception that owner and repository must be supplied together.

        :param filter: accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :type filter: str
        :param state: accepted values: ('open', 'closed')
            api-default: 'open'
        :type state: str
        :param labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :type labels: str
        :param sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :type sort: str
        :param direction: accepted values: ('asc', 'desc')
            api-default: desc
        :type direction: str
        :param since: ISO 8601 formatted timestamp, e.g.,
            2012-05-20T23:10:27Z
        :type since: str
        :returns: list of :class:`Issue <github3.issue.Issue>`\ s
        """
        url = [self._github_url]
        if owner and repository:
            repo = self.repository(owner, repository)
            issues = repo.list_issues()
        else:
            url.append('issues')
            url = '/'.join(url)
            params = issue_params(filter, state, labels, sort, direction,
                    since)
            if params:
                url = '{0}?{1}'.format(url, params)

            json = self._get(url)
            ses = self._session
            issues = [Issue(issue, ses) for issue in json]
        return issues

    def list_keys(self):
        """List public keys for the authenticated user.
        
        :returns: list of :class:`Key <github3.user.Key>`\ s
        """
        url = self._github_url + '/user/keys'
        json = self._get(url)
        ses = self._session
        return [Key(key, ses) for key in json]

    def list_orgs(self, login=None):
        """List public organizations for login if provided; otherwise
        list public and private organizations for the authenticated
        user.
        
        :param login: (optional), user whose orgs you wish to list
        :type login: str
        :returns: list of :class:`Organization <github3.org.Organization>`\ s
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login, 'orgs'])
        else:
            url.extend(['user', 'orgs'])
        url = '/'.join(url)

        json = self._get(url)
        ses = self._session
        return [Organization(org, ses) for org in json]

    def list_repos(self, login=None, type='', sort='', direction=''):
        """List public repositories for the specified ``login`` or all 
        repositories for the authenticated user if ``login`` is not 
        provided.

        :param login: (optional)
        :type login: str
        :param type: (optional), accepted values:
            ('all', 'owner', 'public', 'private', 'member')
            API default: 'all'
        :type type: str
        :param sort: (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :type sort: str
        :param direction: (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :type direction: str
        :returns: list of :class:`Repository <github3.repo.Repository>` 
        objects
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login, 'repos'])
        else:
            url.extend(['user', 'repos'])
        url = '/'.join(url)
        
        params = {}
        if type in ('all', 'owner', 'public', 'private', 'member'):
            params.update(type=type)
        if not login:
            if sort in ('created', 'updated', 'pushed', 'full_name'):
                params.update(sort=sort)
            if direction in ('asc', 'desc'):
                params.update(direction=direction)

        json = self._get(url, params=params)
        ses = self._session
        return [Repository(repo, ses) for repo in json]

    def list_watching(self, login=None):
        """List the repositories being watched by ``login`` if provided or the
        repositories being watched by the authenticated user.

        :param login: (optional)
        :type login: str
        :returns: list of :class:`Repository <github3.repo.Repository>` 
        objects
        """
        if login:
            url = self._github_url + '/users/' + login + '/watched'
        else:
            url = self._github_url + '/user/watched'
        json = self._get(url)
        return [Repository(repo, self._session) for repo in json]

    def login(self, username=None, password=None, token=None):
        """Logs the user into GitHub for protected API calls.
        
        :param username: (optional)
        :type username: str
        :param password: (optional)
        :type password: str
        :param token: (optional)
        :type token: str
        """
        if username and password:
            self._session.auth = (username, password)
        elif token:
            self._session.headers.update({
                'Authorization': 'token ' + token
                })

    def organization(self, login):
        """Returns a Organization object for the login name
        
        :param login: (required), login name of the org
        :type login: str
        :returns: :class:`Organization <org.Organization>`
        """
        url = '{0}/orgs/{1}'.format(self._github_url, login)
        json = self._get(url)
        return Organization(json, self._session) if json else None

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of
        owner and repository
        
        :param owner: (required)
        :type owner: str
        :param repository: (required)
        :type repository: str
        :returns: :class:`Repository <github3.repo.Repository>`
        """
        url = '/'.join([self._github_url, 'repos', owner, repository])
        json = self._get(url)
        return Repository(json, self._session) if json else None

    def search_issues(self, owner, repo, state, keyword):
        """Find issues by state and keyword.

        :param owner: (required)
        :type owner: str
        :param repo: (required)
        :type repo: str
        :param state: (required), accepted values: ('open', 'closed')
        :type state: str
        :param keyword: (required), what to search for
        :type keyword: str
        :returns: None
        """
        pass

    def unfollow(self, login):
        """Make the authenticated user stop following login
        
        :param login: (required)
        :type login: str
        :returns: bool
        """
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._delete(url)
        return resp

    def update_user(self, name=None, email=None, blog=None,
            company=None, location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters. All parameters are
        optional.

        :param name: e.g., 'John Smith', not login name
        :type name: str
        :param email: e.g., 'john.smith@example.com'
        :type email: str
        :param blog: e.g., 'http://www.example.com/jsmith/blog'
        :type blog: str
        :param company: company name
        :type company: str
        :param location: where you are located
        :type location: str
        :param hireable: defaults to False
        :type hireable: bool
        :param bio: GitHub flavored markdown
        :type bio: str
        :returns: bool
        """
        user = self.user()
        if user:
            return user.update(name, email, blog, company, location,
                    hireable, bio)
        return False

    def user(self, login=None):
        """Returns a User object for the specified login name if
        provided. If no login name is provided, this will return a User
        object for the authenticated user.
        
        :param login: (optional)
        :type login: str
        :returns: :class:`User <github3.user.User>`
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login])
        else:
            url.append('user')
        url = '/'.join(url)

        json = self._get(url)
        return User(json, self._session) if json else None

    def watch(self, login, repo):
        """Make user start watching login/repo.
        
        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        resp = False
        if login and repo:
            url = self._github_url + '/user/watched/' + login + '/' + repo
            resp = self._put(url)
        return resp

    def unwatch(self, login, repo):
        """Make user stop watching login/repo.

        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        resp = False
        if login and repo:
            url = self._github_url + '/user/watched/' + login + '/' + repo
            resp = self._delete(url)
        return resp
