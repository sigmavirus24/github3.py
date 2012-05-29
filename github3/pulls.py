"""
github3.pulls
=============

This module contains all the classes relating to pull requests.

"""

from json import dumps
from .git import Commit
from .models import GitHubCore
from .user import User


class PullDestination(GitHubCore):
    def __init__(self, dest, direction):
        super(PullDestination, self).__init__(None)
        self._dir = direction
        self._ref = dest.get('ref')
        self._label = dest.get('label')
        self._user = None
        if dest.get('user'):
            self._user = User(dest.get('user'), None)
        self._sha = dest.get('sha')
        self._repo_name = ''
        self._repo_owner = ''
        if dest.get('repo'):
            self._repo_name = dest['repo'].get('name')
            self._repo_owner = dest['repo']['owner'].get('login')

    def __repr__(self):
        return '<%s [%s]>' % (self._dir, self._label)

    @property
    def label(self):
        return self._label

    @property
    def sha(self):
        return self._sha

    @property
    def ref(self):
        return self._ref

    @property
    def repo(self):
        return (self._repo_owner, self._repo_name)

    @property
    def user(self):
        return self._user


class PullFile(object):
    def __init__(self, pfile):
        super(PullFile, self).__init__()
        self._sha = pfile.get('sha')
        self._name = pfile.get('filename')
        self._status = pfile.get('status')
        self._add = pfile.get('additions')
        self._del = pfile.get('deletions')
        self._changes = pfile.get('changes')
        self._blob = pfile.get('blob_url')
        self._raw = pfile.get('raw_url')
        self._patch = pfile.get('patch')

    def __repr__(self):
        return '<Pull Request File [%s]>' % self._name

    @property
    def additions(self):
        return self._add

    @property
    def blob_url(self):
        return self._blob

    @property
    def changes(self):
        return self._changes

    @property
    def deletions(self):
        return self._del

    @property
    def filename(self):
        return self._name

    @property
    def patch(self):
        return self._patch

    @property
    def raw_url(self):
        return self._raw

    @property
    def sha(self):
        return self._shaw

    @property
    def status(self):
        return self._status


class PullRequest(GitHubCore):
    def __init__(self, pull, session):
        super(PullRequest, self).__init__(session)
        self._update_(pull)

    def __repr__(self):
        return '<Pull Request [#%d]>' % self._num

    def _update_(self, pull):
        self._api_url = pull.get('url')
        self._base = PullDestination(pull.get('base'), 'Base')
        self._body = pull.get('body')

        self._closed = None
        # If the pull request has been closed
        if pull.get('closed_at'):
            self._closed = self._strptime(pull.get('closed_at'))

        self._created = self._strptime(pull.get('created_at'))
        self._diff = pull.get('diff_url')
        self._head = PullDestination(pull.get('head'), 'Head')
        self._url = pull.get('html_url')
        self._id = pull.get('id')
        self._issue = pull.get('issue_url')

        # These are the links provided by the dictionary in the json called
        # '_links'. It's structure is horrific, so to make this look a lot
        # cleaner, I reconstructed what the links would be:
        #  - ``self`` is just the api url, e.g.,
        #    https://api.github.com/repos/:user/:repo/pulls/:number
        #  - ``comments`` is just the api url for comments on the issue, e.g.,
        #    https://api.github.com/repos/:user/:repo/issues/:number/comments
        #  - ``issue`` is the api url for the issue, e.g.,
        #    https://api.github.com/repos/:user/:repo/issues/:number
        #  - ``html`` is just the html_url attribute
        #  - ``review_comments`` is just the api url for the pull, e.g.,
        #    https://api.github.com/repos/:user/:repo/pulls/:number/comments
        self._links = {
                'self': self._api_url,
                'comments': '/'.join([self._api_url.replace('pulls', 'issues'),
                    'comments']),
                'issue': self._api_url.replace('pulls', 'issues'),
                'html': self._url,
                'review_comments': '/'.join([self._api_url, 'comments'])
                }

        self._merged = None
        # If the pull request has been merged
        if pull.get('merged_at'):
            self._merged = self._strptime(pull.get('merged_at'))
        self._num = pull.get('number')
        self._patch_url = pull.get('patch_url')
        self._state = pull.get('state')
        self._title = pull.get('title')
        self._updated = self._strptime(pull.get('updated_at'))
        self._user = None
        if pull.get('user'):
            self._user = User(pull.get('user'), self._session)

    @property
    def base(self):
        return self._base

    @property
    def body(self):
        return self._body

    @property
    def closed_at(self):
        return self._closed

    @property
    def created_at(self):
        return self._created

    @property
    def diff_url(self):
        return self._diff

    @property
    def head(self):
        return self._head

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    def is_merged(self):
        url = '/'.join([self._api_url, 'merge'])
        resp = self._get(url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def issue_url(self):
        return self._issue

    @property
    def links(self):
        return self._links

    def list_commits(self):
        """List the commits on this pull request."""
        url = '/'.join([self._api_url, 'commits'])
        resp = self._get(url)
        commits = []
        if resp.status_code == 200:
            for commit in resp.json:
                commits.append(Commit(commit))

        return commits

    def list_files(self):
        """List the files associated with this pull request."""
        url = '/'.join([self._api_url, 'files'])
        resp = self._get(url)
        files = []
        if resp.status_code == 200:
            for f in resp.json:
                files.append(PullFile(f))
        return files

    def merge(self, commit_message=''):
        """Merge this pull request.

        :param commit_message: (optional), string
        """
        data = {'commit_message': commit_message} if commit_message else None
        url = '/'.join([self._api_url, 'merge'])
        resp = self._put(url, data)
        if resp.status_code == 200:
            return resp.json['merged']
        return resp.json['merged']

    @property
    def merged_at(self):
        return self._merged

    @property
    def number(self):
        return self._num

    @property
    def patch_url(self):
        return self._patch_url

    @property
    def state(self):
        return self._state

    @property
    def title(self):
        return self._title

    def update(self, title='', body='', state=''):
        """Update this pull request.

        :param title: (optional), string
        :param body: (optional), string
        :param state: (optional), string, ('open', 'closed')
        """
        data = dumps({'title': title, 'body': body, 'state': state})
        resp = self._patch(self._api_url, data)
        if resp.status_code == 200:
            self._update_(resp.json)
            return True
        return False

    @property
    def user(self):
        return self._user
