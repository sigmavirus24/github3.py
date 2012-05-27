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
from .repo import Repository
from .user import User, Key


class GitHub(GitHubCore):
    """Stores all the session information."""
    def __init__(self):
        super(GitHub, self).__init__()
        self._session = session()
        # Only accept JSON responses
        self._session.headers.update({'Accept': 'application/json'})
        # Only accept UTF-8 encoded data
        self._session.headers.update({'Accept-Charset': 'utf-8'})

    def __repr__(self):
        return '<github3-session at 0x%x>' % id(self)

    def _list_follow(self, login, which):
        url = [self._github_url]
        if login:
            url.extend(['users', login, which])
        else:
            url.extend(['user', which])
        url = '/'.join(url)

        follow = []
        req = self._get(url)
        if req.status_code == 200:
            for follower in req.json:
                follow.append(User(follower, self._session))
        return follow

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        url = '/'.join([self._github_url, 'gists'])
        response = self._post(url, dumps(new_gist))

        gist = None
        if response.status_code == 201:
            gist = Gist(response.json, self._session)

        return gist

    def create_key(self, title, key):
        """Create a new key for the authenticated user."""
        created = None

        if title and key:
            url = '/'.join([self._github_url, 'user', 'keys'])
            resp = self._post(url, dumps({'title': title, 'key': key}))
            if resp.status_code == 201:
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

        :param owner:
        :param repository:
        :param title: Title of issue to be created
        :param body: The text of the issue, markdown formatted
        :param assignee: Login of person to assign the issue to
        :param milestone: Which milestone to assign the issue to
        :param labels: List of label names.
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

    def delete_key(self, key_id):
        key = self.get_key(key_id)
        if key:
            return key.delete()
        return False

    def follow(self, login):
        """Make the authenticated user follow login."""
        if login:
            print(login)
            url = '/'.join([self._github_url, 'user', 'following', 
                login])
            resp = self._put(url)
            if resp.status_code == 204:
                return True
        return False

    def get_key(self, id_num):
        """Gets the authenticated user's key specified by id_num."""
        if int(id_num) > 0:
            url = '/'.join([self._github_url, 'user', 'keys', 
                str(id_num)])
            resp = self._get(url)
            if resp.status_code == 200:
                return Key(resp.json, self._session)
        return None

    def gist(self, id_num):
        """Gets the gist using the specified id number."""
        url = '/'.join([self._github_url, 'gists', str(id_num)])
        req = self._get(url)
        gist = None
        if req.status_code == 200:
            gist = Gist(req.json, self._session)

        return gist

    def is_following(self, login):
        """Check if the authenticated user is following login."""
        if login:
            url = '/'.join([self._github_url, 'user', 'following', 
                login])
            resp = self._get(url)
            if resp.status_code == 204:
                return True
        return False

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

        req = self._get(url)

        gists = []
        for d in req.json:
            gists.append(Gist(d, self._session))

        return gists

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
                url = '?'.join([url, params])

            issues = []
            req = self._get(url)
            if req.status_code == 200:
                for issue in req.json:
                    issues.append(Issue(issue, self._session))

        return issues

    def list_keys(self):
        """List public keys for the authenticated user."""
        url = '/'.join([self._github_url, 'user', 'keys'])
        resp = self._get(url)
        keys = []
        if resp.status_code == 200:
            for key in resp.json:
                keys.append(Key(key, self._session))
        return keys

    def login(self, username, password):
        """Logs the user into GitHub for protected API calls."""
        self._session.auth = (username, password)

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of
        owner and repository"""
        url = '/'.join([self._github_url, 'repos', owner, repository])
        req = self._get(url)
        if req.status_code == 200:
            return Repository(req.json, self._session)
        return None

    def unfollow(self, login):
        """Make the authenticated user stop following login"""
        if login:
            url = '/'.join([self._github_url, 'user', 'following', 
                login])
            resp = self._delete(url)
            if resp.status_code == 204:
                return True
        return False

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

        req = self._get(url)
        if req.status_code == 200:
            return User(req.json, self._session)
        return None
