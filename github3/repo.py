"""
github3.repo
============

This module contains the class relating to repositories.

"""

from datetime import datetime
from json import dumps
from .issue import Issue, Label, Milestone, issue_params
from .models import GitHubCore
from .user import User


class Repository(GitHubCore):
    """A class to represent how GitHub sends information about repositories."""
    def __init__(self, repo, session):
        super(Repository, self).__init__(session)
        # Clone url using Smart HTTP(s)
        self._https_clone = repo.get('clone_url')
        self._created = self._strptime(repo.get('created_at'))
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
        self._pushed = self._strptime(repo.get('pushed_at'))
        self._size = repo.get('size')

        # SSH url e.g. git@github.com/sigmavirus24/github3.py
        self._ssh = repo.get('ssh_url')
        self._svn = repo.get('svn_url')
        self._updated = self._strptime(repo.get('updated_at'))
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

        resp = self._post(url, issue)
        issue = None
        if resp.status_code == 201:
            issue = Issue(resp.json, self._session)

        return issue

    def create_label(self, name, color):
        label = None

        if color[0] == '#':
            color = color[1:]

        url = '/'.join([self._api_url, 'labels'])
        resp = self._post(url, dumps({'name': name, 'color': color}))

        if resp.status_code == 201:
            label = Label(resp.json, self._session)
        return label

    def create_milestone(self, title, state=None, description=None,
            due_on=None):
        url = '/'.join([self._api_url, 'milestones'])
        mile = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        milestone = None

        resp = self._post(url, mile)
        if resp.status_code == 201:
            milestone = Milestone(resp.json, self._session)

        return milestone

    @property
    def created_at(self):
        return self._created

    @property
    def description(self):
        return self._desc

    def fork(self, organization=None):
        """Create a fork of this repository.

        :param organization: login for organization to create the fork
            under"""
        url = '/'.join([self._api_url, 'forks'])
        if organization:
            resp = self._post(url, dumps({'org': organization}))
        else:
            resp = self._post(url)

        if resp.status_code == 202:
            return Repository(resp.json, self._session)

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

    def issue(self, number):
        if number > 0:
            url = '/'.join([self._api_url, 'issues', str(number)])
            resp = self._get(url)
            if resp.status_code == 200:
                return Issue(resp.json, self._session)

        return None

    def label(self, name):
        if name:
            url = '/'.join([self._api_url, 'labels', name])
            resp = self._get(url)
            if resp.status_code == 200:
                return Label(resp.json, self._session)

        return None

    @property
    def language(self):
        return self._lang

    def list_issues(self,
        milestone=None,
        state=None,
        assignee=None,
        mentioned=None,
        labels=None,
        sort=None,
        direction=None,
        since=None):
        """List issues on this repo based upon parameters passed.

        :param milestone: must be an integer, 'none', or '*'
        :param state: accepted values: ('open', 'closed')
        :param assignee: 'none', '*', or login name
        :param mentioned: user's login name
        :param labels: comma-separated list of labels, e.g. 'bug,ui,@high'
        :param sort: accepted values:
            ('created', 'updated', 'comments', 'created')
        :param direction: accepted values: ('open', 'closed')
        :param since: ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        """
        url = '/'.join([self._api_url, 'issues'])

        params = []
        if milestone in ('*', 'none') or isinstance(milestone, int):
            params.append('milestone=%s' % str(milestone).lower())
            # str(None) = 'None' which is invalid, so .lower() it to make it
            # work.

        if assignee:
            params.append('assignee=%s' % assignee)

        if mentioned:
            params.append('mentioned=%s' % mentioned)

        tmp = issue_params(None, state, labels, sort, direction, since)

        params = '&'.join(params) if params else None
        params = '&'.join([tmp, params]) if params else tmp

        if params:
            url = '?'.join([url, params])

        resp = self._get(url)
        issues = []
        if resp.status_code == 200:
            for issue in resp.json:
                issues.append(Issue(issue, self._session))

        return issues

    def list_labels(self):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._get(url)

        labels = []
        if resp.status_code == 200:
            for label in resp.json:
                labels.append(Label(label, self._session))

        return labels

    def list_milestones(self, state=None, sort=None, direction=None):
        url = '/'.join([self._api_url, 'milestones'])

        params = []
        if state in ('open', 'closed'):
            params.append('state=%s' % state)

        if sort in ('due_date', 'completeness'):
            params.append('sort=%s' % sort)

        if direction in ('asc', 'desc'):
            params.append('direction=%s' % direction)

        if params:
            params = '&'.join(params)
            url = '?'.join([url, params])

        resp = self._get(url)
        milestones = []
        if resp.status_code == 200:
            for mile in resp.json:
                milestones.append(Milestone(mile, self._session))

        return milestones

    def milestone(self, number):
        url = '/'.join([self._api_url, 'milestones', str(number)])
        resp = self._session.get(url)
        if resp.status_code == 200:
            return Milestone(resp.json, self._session)
        return None

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

    def update_label(self, name, color, new_name=''):
        label = self.get_label(name)

        if label:
            if not new_name:
                return label.update(name, color)
            return label.update(new_name, color)

        # label == None
        return False

    @property
    def watchers(self):
        return self._watchers
