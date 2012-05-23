"""
github3.issue
=============

This module contains the classes related to issues.

"""

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
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def name(self):
        return self._name

    def update(self, name, color):
        if color[0] == '#':
            color = color[1:]

        resp = self._patch(self._api_url, dumps({'name': name,
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
        self._created = self._strptime(mile.get('created_at'))
        self._due = None
        if mile.get('due_on'):
            self._due = self._strptime(mile.get('due_on'))

    @property
    def closed_issues(self):
        return self._closed

    @property
    def created_at(self):
        return self._created

    @property
    def creator(self):
        return self._creator

    def delete(self):
        """Delete this milestone."""
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def description(self):
        return self._desc

    @property
    def due_on(self):
        return self._due

    def list_labels(self):
        """List the labels for every issue associated with this
        milestone."""
        url = '/'.join([self._api_url, 'labels'])
        resp = self._get(url)
        labels = []
        if resp.status_code == 200:
            for label in loads(resp.content):
                labels.append(Label(label, self._session))
        return labels

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
        resp = self._patch(self._api_url, inp)
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
            self._closed = self._strptime(issue.get('closed_at'))

        # Numer of comments
        self._comments = issue.get('comments')
        self._created = self._strptime(issue.get('created_at'))
        self._url = issue.get('html_url')
        self._id = issue.get('id')
        self._labels = [Label(l, self._session) for l in issue.get('labels')]

        # Don't want to pass a NoneType to Milestone.__init__()
        if issue.get('milestone'):
            self._mile = Milestone(issue.get('milestone'), self._session)
        self._num = issue.get('number')
        self._pull_req = issue.get('pull_request')
        m = match('https://github\.com/(\S+)/(\S+)/issues/\d+', self._url)
        self._repo = m.groups()
        self._state = issue.get('state')
        self._title = issue.get('title')
        self._updated = self._strptime(issue.get('updated_at'))
        self._api_url = issue.get('url')
        self._user = User(issue.get('user'), self._session)

    def add_labels(self, *args):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._post(url, dumps(args))
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

    def comment(self, id_num):
        """Get a single comment by its id.

        The catch here is that id is NOT a simple number to obtain. If
        you were to look at the comments on issue #15 in
        sigmavirus24/Todo.txt-python, the first comment's id is 4150787.
        """
        if id_num > 0:  # Might as well check that it's positive
            url = '/'.join([self._github_url, self._repo[0],
                self._repo[1], 'issues', 'comments', str(id)])
            resp = self._get(url)
            if resp.status_code == 200:
                return IssueComment(loads(resp.content))
        return None

    @property
    def comments(self):
        return self._comments

    def create_comment(self, body):
        """Create a comment on this issue."""
        if body:
            url = '/'.join([self._api_url, 'comments'])
            resp = self._post(url, dumps({'body': body}))
            if resp.status_code == 201:
                return True

        return False

    @property
    def created_at(self):
        return self._created

    def edit(self, title=None, body=None, assignee=None, state=None,
            milestone=None, labels=[]):
        """Edit this issue.

        :param title: Title of the issue, string
        :param body: markdown formatted string
        :param assignee: login name of user the issue should be assigned to
        :param state: ('open', 'closed')
        :param milestone: the NUMBER (not title) of the milestone to assign
            this to [1]_
        :param labels: list of labels to apply this to

        .. [1] Milestone numbering starts at 1, i.e. the first milestone you
               create is 1, the second is 2, etc.
        """
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels}
        resp = self._patch(self._api_url, dumps(data))
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

    def list_comments(self):
        url = '/'.join([self._api_url, 'comments'])
        resp = self._get(url)

        comments = []
        if resp.status_code == 200:
            for comment in loads(resp.content):
                comments.append(IssueComment(comment, self._session))
        return comments

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
        resp = self._delete(url)
        if resp.status_code == 200:
            return True
        return False

    def remove_all_labels(self):
        # Can either send DELETE or [] to remove all labels
        return self.replace_labels([])

    def replace_labels(self, labels):
        url = '/'.join([self._api_url, 'labels'])
        resp = self._put(url, dumps(labels))
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


class IssueComment(BaseComment):
    def __init__(self, comment, session):
        super(IssueComment, self).__init__(comment, session)

    def __repr__(self):
        return '<Issue Comment [%s]>' % self._user.login

    @property
    def updated_at(self):
        return self._updated


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
