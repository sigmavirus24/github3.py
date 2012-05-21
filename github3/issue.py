"""
github3.issue
=============

This module contains the classes related to issues.
"""

from datetime import datetime
from json import dumps
from re import match
from .models import GitHubCore, BaseComment, User
from .compat import loads


class Label(GitHubCore):
    def __init__(self, label, session):
        super(Label, self).__init__(session)
        self._update_(label)

    def __repr__(self):
        return '<Label [%s]>' % self._name

    def _update_(self, label):
        self._api_url = label.get('url')
        self._color = label.get('color')
        self._name = label.get('name')

    @property
    def color(self):
        return self._color

    def delete(self):
        resp = self._session.delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def name(self):
        return self._name

    def update(self, name, color):
        if color[0] == '#':
            color = color[1:]

        resp = self._session.patch(self._api_url, dumps({'name': name,
            'color': color}))
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True

        return False


class Repository(GitHubCore):
    """A class to represent how GitHub sends information about repositories."""
    def __init__(self, repo, session):
        super(Repository, self).__init__(session)
        # Clone url using Smart HTTP(s)
        self._https_clone = repo.get('clone_url')
        self._created = datetime.strptime(repo.get('created_at'),
                self._time_format)
        self._desc = repo.get('description')

        # The number of forks
        self._forks = repo.get('forks')

        # Is this repository a fork?
        self._is_fork = repo.get('fork')

        # Clone url using git, e.g. git://github.com/sigmavirus24/github3.py
        self._git_clone = repo.get('git_url')
        self._has_dl = repo.get('has_downloads')
        self._has_issues = repo.get('has_issues')
        self._has_wiki = repo.get('has_wiki')

        # e.g. https://sigmavirus24.github.com/github3.py
        self._homepg = repo.get('homepage')

        # e.g. https://github.com/sigmavirus24/github3.py
        self._url = repo.get('html_url')
        self._id = repo.get('id')
        self._lang = repo.get('lang')
        self._mirror = repo.get('mirror_url')

        # Repository name, e.g. github3.py
        self._name = repo.get('name')

        # Number of open issues
        self._open_issues = repo.get('open_issues')

        # Repository owner's name
        self._owner = User(repo.get('owner'), self._session)

        # Is this repository private?
        self._priv = repo.get('private')
        self._pushed = datetime.strptime(repo.get('pushed_at'),
                self._time_format)
        self._size = repo.get('size')

        # SSH url e.g. git@github.com/sigmavirus24/github3.py
        self._ssh = repo.get('ssh_url')
        self._svn = repo.get('svn_url')
        self._updated = datetime.strptime(repo.get('updated_at'),
                self._time_format)
        self._api_url = repo.get('url')

        # The number of watchers
        self._watch = repo.get('watchers')

    def __repr__(self):
        return '<Repository [%s/%s]>' % (self._owner, self._name)

    @property
    def clone_url(self):
        return self._https_clone

    def create_issue(self,
        title,
        body=None,
        assignee=None,
        milestone=None,
        labels=[]):
        """Creates an issue on this repository."""
        issue = dumps({'title': title, 'body': body,
            'assignee': assignee, 'milestone': milestone, 
            'labels': labels})
        url = '/'.join([self._api_url, 'issues'])

        resp = self._session.post(url, issue)
        if resp.status_code == 201:
            return True
        return False

    def create_label(self, name, color):
        if color[0] == '#':
            color = color[1:]
        url = '/'.join([self._github_url, 'repos', self._repo_owner,
            self._repo_name, 'labels'])
        resp = self._session.post(url, dumps({'name': name, 'color': color}))
        if resp.status_code == 201:
            return True
        return False

    @property
    def created_at(self):
        return self._created

    @property
    def description(self):
        return self._desc

    def fork(self, organization=None):
        """Create a fork of this repository.
        
        :param organization: login for organization to create the fork under"""
        url = '/'.join([self._api_url, 'forks'])
        if organization:
            resp = self._session.post(url, dumps({'org': organization}))
        else:
            resp = self._session.post(url)

        if resp.status_code == 202:
            return Repository(loads(resp.content), self._session)

        return None

    @property
    def forks(self):
        return self._forks

    def is_fork(self):
        return self._is_fork

    @property
    def git_clone(self):
        return self._git_clone

    def has_downloads(self):
        return self._has_dl

    def has_wiki(self):
        return self._has_wiki

    @property
    def homepage(self):
        return self._homepg

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    def get_label(self, name):
        label = None
        
        if name:
            url = '/'.join([self._github_url, self._repo_owner, self._repo_name,
                'labels', name])
            resp = self._session.get(url)
            if resp.status_code == 200:
                label = Label(loads(resp.content), self._session)

        return label

    @property
    def language(self):
        return self._lang

    def list_labels(self):
        url = '/'.join([self._github_url, 'repos', self._repo_owner,
            self._repo_name, 'labels'])
        resp = self._session.get(url)

        labels = []
        if resp.status_code == 200:
            jlabels = loads(resp.content)
            for jlabel in jlabels:
                labels.append(Label(jlabel, self._session))

        return labels

    @property
    def mirror(self):
        return self._mirror

    @property
    def name(self):
        return self._name

    @property
    def open_issues(self):
        return self._open_issues

    @property
    def owner(self):
        return self._owner

    def is_private(self):
        return self._priv

    @property
    def pushed_at(self):
        return self._pushed

    @property
    def size(self):
        return self._size

    @property
    def ssh_url(self):
        return self._ssh

    @property
    def svn_url(self):
        return self._svn

    @property
    def updated_at(self):
        return self._updated

    def update_label(self, name, color, new_name=None):
        label = self.get_label(name)

        if label:
            if not new_name:
                return label.edit(name, color)
            return label.edit(new_name, color)

        # label == None
        return False

    @property
    def watchers(self):
        return self._watchers


class Issue(GitHubCore):
    def __init__(self, issue, session):
        super(Issue, self).__init__(session)
        self._update_(issue)

    def __repr__(self):
        return '<Issue [%s/%s #%s]>' % (self._repo_owner, self._repo_name,
                self._num)

    def _update_(self, issue):
        if issue.get('assignee'):
            self._assign = User(issue.get('assignee'), self._session)
        self._body = issue.get('body')

        # If an issue is still open, this field will be None
        self._closed = None
        if issue.get('closed_at'):
            self._closed = datetime.strptime(issue.get('closed_at'),
                self._time_format)

        # Numer of comments
        self._comments = issue.get('comments')
        self._created = datetime.strptime(issue.get('created_at'),
                self._time_format)
        self._url = issue.get('html_url')
        self._id = issue.get('id')
        self._labels = [Label(label, self._session) for label in issue.get('labels')]
        self._mile = issue.get('milestone')
        self._num = issue.get('number')
        self._pull_req = issue.get('pull_request')
        self._repo = None
        if issue.get('repository'):
            self._repo = Repository(issue.get('repository'), self._session)
            self._repo_name = self._repo.name
            self._repo_owner = self._repo.owner.login
            self._repo._session = self._session
        else:
            m = match('https://github\.com/(\S+)/(\S+)/issues/\d+', self._url)
            self._repo_owner = m.groups()[0]
            self._repo_name = m.groups()[1]
        self._state = issue.get('state')
        self._title = issue.get('title')
        self._updated = datetime.strptime(issue.get('updated_at'),
                self._time_format)
        self._api_url = issue.get('url')
        self._user = User(issue.get('user'), self._session)

    def add_labels(self, *args):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._session.post(url, dumps(args))
        if resp.status_code == 200:
            return True
        return False

    @property
    def assignee(self):
        return self._assign

    @property
    def body(self):
        return self._body

    def close(self):
        return self.edit(self._title, self._body, self._assign.login, 
                'closed', self._mile, self._labels)

    @property
    def closed_at(self):
        return self._closed

    @property
    def comments(self):
        return self._comments

    @property
    def created_at(self):
        return self._created

    def edit(self, title=None, body=None, assignee=None, state=None,
            milestone=None, labels=[]):
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels}
        resp = self._session.patch(self._api_url, dumps(data))
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True

        return False

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    def is_closed(self):
        if self._closed or (self._state == 'closed'):
            return True
        return False

    @property
    def labels(self):
        return self._labels

    @property
    def milestone(self):
        return self._mile

    @property
    def number(self):
        return self._num

    @property
    def pull_request(self):
        return self._pull_req

    def remove_label(self, name):
        url = '/'.join([self._api_url, 'labels', name])
        resp = self._session.delete(url)
        if resp.status_code == 200:
            return True
        return False

    def remove_all_labels(self):
        # Can either send DELETE or [] to remove all labels
        return self.replace_labels([])

    def replace_labels(self, labels):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._session.put(url, dumps(labels))
        if resp.status_code == 200:
            return True
        return False

    def reopen(self):
        return self.edit(self._title, self._body, self._assign.login, 
                'open', self._mile, self._labels)

    @property
    def repository(self):
        return self._repo

    @property
    def state(self):
        return self._state

    @property
    def title(self):
        return self._title

    @property
    def updated_at(self):
        return self._updated

    @property
    def user(self):
        return self._user
