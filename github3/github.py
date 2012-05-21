"""
github3.github
==============

This module contains the main GitHub session object.

"""

from requests import session
from json import dumps
from .compat import loads
from .models import GitHubCore
from .issue import Issue, issue_params
from .repo import Repository
from .gist import Gist


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

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        _url = '/'.join([self._github_url, 'gists'])
        response = self._session.post(_url, dumps(new_gist))

        gist = None
        if response.status_code == 201:
            gist = Gist(loads(response.content), self._session)

        return gist

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
        return False

    def gist(self, id_num):
        """Gets the gist using the specified id number."""
        url = '/'.join([self._github_url, 'gists', str(id_num)])
        req = self._session.get(url)
        gist = None
        if req.status_code == 200:
            gist = Gist(loads(req.content), self._session)

        return gist

    def gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists"""
        _url = [self._github_url]
        if username:
            _url.extend(['users', username, 'gists'])
        else:
            _url.append('gists')
        url = '/'.join(_url)

        req = self._session.get(url)
        data = loads(req.content)

        gists = []
        for d in data:
            gists.append(Gist(d, self._session))

        return gists

    def issue(self, owner, repository, number):
        """Fetch issue #:number: from 
        https://github.com/:owner:/:repository:"""
        url = '/'.join([self._github_url, 'repos', owner, repository, 'issues',
            str(number)])
        req = self._session.get(url)
        issue = None
        if req.status_code == 200:
            issue = Issue(loads(req.content), self._session)

        return issue

    def issues(self,
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
            url.extend(['repos', owner, repository, 'issues'])
        else:
            url.append('issues')
        url = '/'.join(url)
        params = issue_params(filter, state, labels, sort, direction, since)
        if params:
            url = '?'.join([url, params])

        issues = []
        req = self._session.get(url)
        if req.status_code == 200:
            jissues = loads(req.content)
            for jissue in jissues:
                issues.append(Issue(jissue, self._session))

        return issues

    def login(self, username, password):
        """Logs the user into GitHub for protected API calls."""
        self._session.auth = (username, password)

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of 
        owner and repository"""
        url = '/'.join([self._github_url, 'repos', owner, repository])
        req = self._session.get(url)
        if req.status_code == 200:
            return Repository(loads(req.content), self._session)
        return None
