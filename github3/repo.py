"""
github3.repo
============

This module contains the class relating to repositories.

"""

from datetime import datetime
from json import dumps
from .compat import loads
from .models import GitHubCore, User
from .issue import Issue, Label  #, Milestone


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
        return '<Repository [%s/%s]>' % (self._owner.login, self._name)

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
        url = '/'.join([self._github_url, 'repos', self._repo[0],
            self._repo[1], 'labels'])
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
            url = '/'.join([self._github_url, self._repo[0], self._repo[1],
                'labels', name])
            resp = self._session.get(url)
            if resp.status_code == 200:
                label = Label(loads(resp.content), self._session)

        return label

    @property
    def language(self):
        return self._lang

    def list_issues(self):
        url = '/'.join([self._api_url, 'issues'])

    def list_labels(self):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._session.get(url)

        labels = []
        if resp.status_code == 200:
            jlabels = loads(resp.content)
            for jlabel in jlabels:
                labels.append(Label(jlabel, self._session))

        return labels

    def list_milestones(self):
        pass

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
