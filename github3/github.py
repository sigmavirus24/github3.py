"""
github3.github
==============

This module contains the main GitHub session object.

"""

from requests import session
from json import dumps
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
        url = [self._github_url]
        if login:
            url.extend(['users', login, which])
        else:
            url.extend(['user', which])
        url = '/'.join(url)

        follow = []
        resp = self._get(url)
        ses = self._session
        return [User(follower, ses) for follower in json]

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        url = self._github_url + '/gists'
        json = self._post(url, dumps(new_gist))
        return Gist(json, self._session) if json else None

    def create_key(self, title, key):
        """Create a new key for the authenticated user."""
        created = None

        if title and key:
            url = self._github_url + '/user/keys'
            json = self._post(url, dumps({'title': title, 'key': key}))
            if json:
                created = Key(resp.json, self._session)
        return created

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

        :param owner: (required), string, login of the owner
        :param repository: (required), string, repository name
        :param title: (required), string, Title of issue to be created
        :param body: (optional), string, The text of the issue, markdown
            formatted
        :param assignee: (optional), string, Login of person to assign
            the issue to
        :param milestone: (optional), string, Which milestone to assign
            the issue to
        :param labels: (optional), list, List of label names.
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

    def create_repo(self,
        name,
        description='',
        homepage='',
        private=False,
        has_issues=True,
        has_wiki=True,
        has_downloads=True):
        """Create a repository for the authenticated user.

        :param name: (required), string, name of the repository
        :param description: (optional), string
        :param homepage: (optional), string
        :param private: (optional), boolean, If ``True``, create a
            private repository. API default: ``False``
        :param has_issues: (optional), boolean, If ``True``, enable
            issues for this repository. API default: ``True``
        :param has_wiki: (optional), boolean, If ``True``, enable the
            wiki for this repository. API default: ``True``
        :param has_downloads: (optional), boolean, If ``True``, enable
            downloads for this repository. API default: ``True``
        """
        url = self._github_url + '/user/repos'
        data = dumps({'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads})
        json = self._post(url, data)
        return Repository(json, self._session) if json else None

    def delete_key(self, key_id):
        key = self.get_key(key_id)
        if key:
            return key.delete()
        return False

    def follow(self, login):
        """Make the authenticated user follow login."""
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._put(url)
        return False

    def get_key(self, id_num):
        """Gets the authenticated user's key specified by id_num."""
        json = None
        if int(id_num) > 0:
            url = '{0}/user/keys/{1}'.format(self._github_url,
                    str(id_num))
            json = self._get(url)
        return Key(json, self._session) if json else None

    def gist(self, id_num):
        """Gets the gist using the specified id number."""
        url = '{0}/gists/{1}'.format(self._github_url, str(id_num))
        json = self._get(url)
        return Gist(json, self._session) if json else None

    def is_following(self, login):
        """Check if the authenticated user is following login."""
        json = None
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url, login)
            json = self._get(url, status_code=204)
        return True if json else False

    def issue(self, owner, repository, number):
        """Fetch issue #:number: from
        https://github.com/:owner:/:repository:"""
        repo = self.repository(owner, repository)
        if repo:
            return repo.issue(number)
        return None

    def list_followers(self, login=None):
        """If login is provided, return a list of followers of that
        login name; otherwise return a list of followers of the
        authenticated user."""
        return self._list_follow(login, 'followers')

    def list_following(self, login=None):
        """If login is provided, return a list of users being followed
        by login; otherwise return a list of people followed by the
        authenticated user."""
        return self._list_follow(login, 'following')

    def list_gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists"""
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
            api-default: assigned
        :param state: accepted values: ('open', 'closed')
            api-default: open
        :param labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :param sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :param direction: accepted values: ('asc', 'desc')
            api-default: desc
        :param since: ISO 8601 formatted timestamp, e.g.,
            2012-05-20T23:10:27Z
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
        """List public keys for the authenticated user."""
        url = self._github_url + '/user/keys'
        json = self._get(url)
        ses = self._session
        return [Key(key, ses) for key in json]

    def list_orgs(self, login=None):
        """List public organizations for login if provided; otherwise
        list public and private organizations for the authenticated
        user."""
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

        :param type: (optional), string, accepted values:
            ('all', 'owner', 'public', 'private', 'member')
            API default: 'all'
        :param sort: (optional), string, accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :param direction: (optional), string, accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login, 'repos'])
        else:
            url.extend(['user', 'repos'])
        url = '/'.join(url)
        
        params = []
        if type in ('all', 'owner', 'public', 'private', 'member'):
            params.append('type={0}'.format(type))
        if not login:
            if sort in ('created', 'updated', 'pushed', 'full_name'):
                params.append('sort={0}'.format(sort))
            if direction in ('asc', 'desc'):
                params.append('direction={0}'.format(sort))
        if params:
            params = '&'.join(params)
            url = '?'.join([url, params])

        json = self._get(url)
        ses = self._session
        return [Repository(repo, ses) for repo in json]

    def login(self, username=None, password=None, token=None):
        """Logs the user into GitHub for protected API calls."""
        if username and password:
            self._session.auth = (username, password)
        elif token:
            self._session.update({'access_token': token})

    def organization(self, login):
        """Returns a Organization object for the login name"""
        url = '{0}/orgs/{1}'.format(self._github_url, login)
        json = self._get(url)
        return Organization(json, self._session) if json else None

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of
        owner and repository"""
        url = '/'.join([self._github_url, 'repos', owner, repository])
        json = self._get(url)
        return Repository(json, self._session) if json else None

    def unfollow(self, login):
        """Make the authenticated user stop following login"""
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._delete(url)
        return resp

    def update_user(self, name=None, email=None, blog=None,
            company=None, location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters.

        :param name: string, e.g., 'John Smith', not login name
        :param email: string, e.g., 'john.smith@example.com'
        :param blog: string, e.g., 'http://www.example.com/jsmith/blog'
        :param company: string
        :param location: string
        :param hireable: boolean, defaults to False
        :param bio: string, GitHub flavored markdown
        """
        user = self.user()
        if user:
            return user.update(name, email, blog, company, location,
                    hireable, bio)
        return False

    def user(self, login=None):
        """Returns a User object for the specified login name if
        provided. If no login name is provided, this will return a User
        object for the authenticated user."""
        url = [self._github_url]
        if login:
            url.extend(['users', login])
        else:
            url.append('user')
        url = '/'.join(url)

        json = self._get(url)
        return User(json, self._session) if json else None
