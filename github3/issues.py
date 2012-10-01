"""
github3.issues
==============

This module contains the classes related to issues.

"""

from json import dumps
from re import match
from github3.models import GitHubCore, BaseComment
from github3.users import User
from github3.decorators import requires_auth


class Label(GitHubCore):
    """The :class:`Label <Label>` object. Succintly represents a label that
    exists in a repository."""
    def __init__(self, label, session=None):
        super(Label, self).__init__(label, session)
        self._api = label.get('url', '')
        #: Color of the label, e.g., 626262
        self.color = label.get('color')
        #: Name of the label, e.g., 'bug'
        self.name = label.get('name')

    def __repr__(self):
        return '<Label [{0}]>'.format(self.name)

    def _update_(self, label):
        self.__init__(label, self._session)

    @requires_auth
    def delete(self):
        """Delete this label.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, name, color):
        """Update this label.

        :param str name: (required), new name of the label
        :param str color: (required), color code, e.g., 626262, no leading '#'
        :returns: bool
        """
        json = None

        if name and color:
            if color[0] == '#':
                color = color[1:]
            json = self._json(self._patch(self._api, data=dumps({'name': name,
                'color': color})), 200)

        if json:
            self._update_(json)
            return True

        return False


class Milestone(GitHubCore):
    """The :class:`Milestone <Milestone>` object. This is a small class to
    handle information about milestones on repositories and issues.
    """
    def __init__(self, mile, session=None):
        super(Milestone, self).__init__(mile, session)
        self._api = mile.get('url', '')
        #: Identifying number associated with milestone.
        self.number = mile.get('number')
        #: State of the milestone, e.g., open or closed.
        self.state = mile.get('state')
        #: Title of the milestone, e.g., 0.2.
        self.title = mile.get('title')
        #: Description of this milestone.
        self.description = mile.get('description')
        #: :class:`User <github3.users.User>` object representing the creator
        #  of the milestone.
        self.creator = User(mile.get('creator'), self._session)
        #: Number of issues associated with this milestone which are still
        #  open.
        self.open_issues = mile.get('open_issues')
        #: The number of closed issues associated with this milestone.
        self.closed_issues = mile.get('closed_issues')
        #: datetime object representing when the milestone was created.
        self.created_at = self._strptime(mile.get('created_at'))
        #: datetime representing when this milestone is due.
        self.due_on = None
        if mile.get('due_on'):
            self.due_on = self._strptime(mile.get('due_on'))

    def __repr__(self):
        return '<Milestone [{0}]>'.format(self.title)

    def _update_(self, mile):
        self.__init__(mile, self._session)

    @requires_auth
    def delete(self):
        """Delete this milestone.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    def iter_labels(self, number=-1):
        """Iterate over the labels for every issue associated with this
        milestone.

        :param int number: (optional), number of labels to return. Default: -1
            returns all available labels.
        :returns: generator of :class:`Label <Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        return self._iter(int(number), url, Label)

    def list_labels(self):
        """List the labels for every issue associated with this
        milestone.

        :returns: list of :class:`Label <Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Label(label, self) for label in json]

    @requires_auth
    def update(self, title, state='', description='', due_on=''):
        """Update this milestone.

        state, description, and due_on are optional

        :param str title: (required), new title of the milestone
        :param str state: (optional), ('open', 'closed')
        :param str description: (optional)
        :param str due_on: (optional), ISO 8601 time format:
            YYYY-MM-DDTHH:MM:SSZ
        :returns: bool
        """
        data = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        json = None

        if title:
            json = self._json(self._patch(self._api, data=data), 200)
        if json:
            self._update_(json)
            return True
        return False


class Issue(GitHubCore):
    """The :class:`Issue <Issue>` object. It structures and handles the data
    returned via the `Issues <http://developer.github.com/v3/issues>`_ section
    of the GitHub API.
    """
    def __init__(self, issue, session=None):
        super(Issue, self).__init__(issue, session)
        self._api = issue.get('url', '')
        #: :class:`User <github3.users.User>` representing the user the issue
        #  was assigned to.
        self.assignee = issue.get('assignee')
        if self.assignee:
            self.assignee = User(issue.get('assignee'), self._session)
        #: Body (description) of the issue.
        self.body = issue.get('body', '')
        #: HTML formatted body of the issue.
        self.body_html = issue.get('body_html', '')
        #: Plain text formatted body of the issue.
        self.body_text = issue.get('body_text', '')

        # If an issue is still open, this field will be None
        #: datetime object representing when the issue was closed.
        self.closed_at = None
        if issue.get('closed_at'):
            self.closed_at = self._strptime(issue.get('closed_at'))

        #: Number of comments on this issue.
        self.comments = issue.get('comments')
        #: datetime object representing when the issue was created.
        self.created_at = self._strptime(issue.get('created_at'))
        #: URL to view the issue at GitHub.
        self.html_url = issue.get('html_url')
        #: Unique ID for the issue.
        self.id = issue.get('id')
        #: Returns the list of :class:`Label <Label>`\ s on this issue.
        self.labels = [Label(l, self._session) for l in issue.get('labels')]

        #: :class:`Milestone <Milestone>` this issue was assigned to.
        self.milestone = None
        if issue.get('milestone'):
            self.milestone = Milestone(issue.get('milestone'), self._session)
        #: Issue number (e.g. #15)
        self.number = issue.get('number')
        #: Dictionary URLs for the pull request (if they exist)
        self.pull_request = issue.get('pull_request')
        m = match('https://github\.com/(\S+)/(\S+)/issues/\d+', self.html_url)
        #: Returns ('owner', 'repository') this issue was filed on.
        self.repository = m.groups()
        #: State of the issue, e.g., open, closed
        self.state = issue.get('state')
        #: Title of the issue.
        self.title = issue.get('title')
        #: datetime object representing the last time the issue was updated.
        self.updated_at = self._strptime(issue.get('updated_at'))
        #: :class:`User <github3.users.User>` who opened the issue.
        self.user = User(issue.get('user'), self._session)

    def __repr__(self):
        return '<Issue [{r[0]}/{r[1]} #{n}]>'.format(r=self.repository,
                n=self.number)

    def _update_(self, issue):
        self.__init__(issue, self._session)

    @requires_auth
    def add_labels(self, *args):
        """Add labels to this issue.

        :param str args: (required), names of the labels you wish to add
        :returns: bool
        """
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._post(url, data=dumps(list(args))),
                status_code=200)
        return True if json else False

    @requires_auth
    def close(self):
        """Close this issue."""
        assignee = ''
        if self.assignee:
            assignee = self.assignee.login
        return self.edit(self.title, self.body, assignee, 'closed',
                self.milestone, self.labels)

    def comment(self, id_num):
        """Get a single comment by its id.

        The catch here is that id is NOT a simple number to obtain. If
        you were to look at the comments on issue #15 in
        sigmavirus24/Todo.txt-python, the first comment's id is 4150787.

        :param int id_num: (required), comment id, see example above
        :returns: :class:`IssueComment <IssueComment>`
        """
        json = None
        if int(id_num) > 0:  # Might as well check that it's positive
            owner, repo = self.repository
            url = self._build_url('repos', owner, repo, 'issues', 'comments',
                    str(id_num))
            json = self._json(self._get(url), 200)
        return IssueComment(json) if json else None

    @requires_auth
    def create_comment(self, body):
        """Create a comment on this issue.

        :param str body: (required), comment body
        :returns: :class:`IssueComment <IssueComment>`
        """
        json = None
        if body:
            url = self._build_url('comments', base_url=self._api)
            json = self._json(self._post(url, dumps({'body': body})), 201)
        return IssueComment(json, self) if json else None

    @requires_auth
    def edit(self, title=None, body=None, assignee=None, state=None,
            milestone=None, labels=None):
        """Edit this issue.

        :param title: Title of the issue
        :type title: str
        :param body: markdown formatted body (description) of the issue
        :type body: str
        :param assignee: login name of user the issue should be assigned to
        :type assignee: str
        :param state: accepted values: ('open', 'closed')
        :type state: str
        :param milestone: the NUMBER (not title) of the milestone to assign
            this to [1]_
        :type milestone: int
        :param labels: list of labels to apply this to
        :type labels: list of str's
        :returns: bool

        .. [1] Milestone numbering starts at 1, i.e. the first milestone you
               create is 1, the second is 2, etc.
        """
        json = None
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels}
        for (k, v) in list(data.items()):
            if v is None:
                del data[k]
        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_(json)
            return True
        return False

    def is_closed(self):
        """Checks if the issue is closed.

        :returns: bool
        """
        if self.closed_at or (self.state == 'closed'):
            return True
        return False

    def iter_comments(self, number=-1):
        """Iterate over the comments on this issue.

        :param int number: (optional), number of comments to iterate over
        :returns: iterator of :class:`IssueComment <IssueComment>`
        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, IssueComment)

    def list_comments(self):
        """List comments on this issue.

        :returns: list of :class:`IssueComment <IssueComment>`
        """
        url = self._build_url('comments', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [IssueComment(comment, self) for comment in json]

    def iter_events(self, number=-1):
        """Iterate over events associated with this issue only.

        :param int number: (optional), number of events to return. Default: -1
            returns all events available.
        :returns: generator of :class:`IssueEvent <IssueEvent>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, IssueEvent)

    def list_events(self):
        """List events associated with this issue only.

        :returns: list of :class:`IssueEvent <IssueEvent>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [IssueEvent(event, self) for event in json]

    @requires_auth
    def remove_label(self, name):
        """Removes label ``name`` from this issue.

        :param str name: (required), name of the label to remove
        :returns: list of labels remaining
        """
        url = self._build_url('labels', name, base_url=self._api)
        return self._json(self._delete(url), 200)

    @requires_auth
    def remove_all_labels(self):
        """Remove all labels from this issue.

        :returns: bool
        """
        # Can either send DELETE or [] to remove all labels
        return self.replace_labels([])

    @requires_auth
    def replace_labels(self, labels):
        """Replace all labels on this issue with ``labels``.

        :param labels: label names
        :type: list of str's
        :returns: bool
        """
        url = self._build_url('labels', base_url=self._api)
        return self._boolean(self._put(url, data=dumps(labels)), 200, 404)

    @requires_auth
    def reopen(self):
        """Re-open a closed issue.

        :returns: bool
        """
        assignee = ''
        if self.assignee:
            assignee = self.assignee.login
        return self.edit(self.title, self.body, assignee, 'open',
                self.milestone, self.labels)


class IssueComment(BaseComment):
    """The :class:`IssueComment <IssueComment>` object. This structures and
    handles the comments on issues specifically.
    """
    def __init__(self, comment, session=None):
        super(IssueComment, self).__init__(comment, session)

        #: :class:`User <github3.users.User>` who made the comment
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)

    def __repr__(self):
        return '<Issue Comment [{0}]>'.format(self.user.login)


class IssueEvent(GitHubCore):
    """The :class:`IssueEvent <IssueEvent>` object. This specifically deals
    with events described in the
    `Issues\>Events <http://developer.github.com/v3/issues/events>`_ section of
    the GitHub API.
    """
    def __init__(self, event, issue=None):
        super(IssueEvent, self).__init__(event, None)
        # The type of event:
        #   ('closed', 'reopened', 'subscribed', 'merged', 'referenced',
        #    'mentioned', 'assigned')
        #: The type of event, e.g., closed
        self.event = event.get('event')
        #: SHA of the commit.
        self.commit_id = event.get('commit_id')
        self._api = event.get('url', '')

        #: :class:`Issue <Issue>` where this comment was made.
        self.issue = issue
        if event.get('issue'):
            self.issue = Issue(event.get('issue'), self)

        #: Number of comments
        self.comments = event.get('comments', 0)

        #: datetime object representing when the event was created.
        self.created_at = self._strptime(event.get('created_at'))

        #: Dictionary of links for the pull request
        self.pull_request = event.get('pull_request', {})

    def __repr__(self):
        return '<Issue Event [#{0} - {1}]>'.format(self.issue.number,
                self.event)


def issue_params(filter, state, labels, sort, direction, since):
    params = {}
    if filter in ('assigned', 'created', 'mentioned', 'subscribed'):
        params['filter'] = filter

    if state in ('open', 'closed'):
        params['state'] = state

    if labels:
        params['labels'] = labels

    if sort in ('created', 'updated', 'comments'):
        params['sort'] = sort

    if direction in ('asc', 'desc'):
        params['direction'] = direction

    if since and match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', since):
        params['since'] = since

    return params
