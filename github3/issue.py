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


class Milestone(GitHubCore):
    def __init__(self, mile, session):
        super(Milestone, self).__init__(session)
        self._update_(mile)

    def __repr__(self):
        return '<Milestone [%s]>' % self._title

    def _update_(self, mile):
        self._api_url = mile.get('url')
        self._num = mile.get('number')
        self._state = mile.get('state')
        self._title = mile.get('title')
        self._desc = mile.get('description')
        self._creator = User(mile.get('creator'), self._session)
        self._open = mile.get('open_issues')
        self._closed = mile.get('closed_issues')
        self._created = datetime.strptime(mile.get('created_at'),
                self._time_format)
        self._due = None
        if mile.get('due_on'):
            self._due = datetime.strptime(mile.get('due_on'), 
                    self._time_format)

    @property
    def closed_issues(self):
        return self._closed

    @property
    def created_at(self):
        return self._created

    @property
    def creator(self):
        return self._creator

    @property
    def description(self):
        return self._desc

    @property
    def due_on(self):
        return self._due

    @property
    def number(self):
        return self._num

    @property
    def open_issues(self):
        return self._open

    @property
    def state(self):
        return self._state

    @property
    def title(self):
        return self._title

    def update(self, title, state=None, description=None, due_on=None):
        """Update this milestone.

        state, description, and due_on are optional

        :param title: *required*, string
        :param state: ('open', 'closed')
        :param description: string
        :param due_on: ISO 8601 time string: YYYY-MM-DDTHH:MM:SSZ
        """
        inp = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        resp = self._session.patch(self._api_url, inp)
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True
        return False


class Issue(GitHubCore):
    def __init__(self, issue, session):
        super(Issue, self).__init__(session)
        self._update_(issue)

    def __repr__(self):
        return '<Issue [%s/%s #%s]>' % (self._repo[0], self._repo[1],
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
        self._mile = Milestone(issue.get('milestone'), self._session)
        self._num = issue.get('number')
        self._pull_req = issue.get('pull_request')
        m = match('https://github\.com/(\S+)/(\S+)/issues/\d+', self._url)
        self._repo = m.groups()
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


def issue_params(filter, state, labels, sort, direction, since):
    params = []
    if filter in ('assigned', 'created', 'mentioned', 'subscribed'):
        params.append('filter=%s' % filter)

    if state in ('open', 'closed'):
        params.append('state=%s' % state)

    if labels:
        params.append('labels=%s' % labels)

    if sort in ('created', 'updated', 'comments'):
        params.append('sort=%s' % sort)

    if direction in ('asc', 'desc'):
        params.append('direction=%s' % direction)

    if since and match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', since):
        params.append('since=%s' % since)

    return '&'.join(params)
