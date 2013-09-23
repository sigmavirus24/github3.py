from re import match
from json import dumps
from github3.decorators import requires_auth
from github3.issues.comment import IssueComment
from github3.issues.event import IssueEvent
from github3.issues.label import Label
from github3.issues.milestone import Milestone
from github3.models import GitHubCore
from github3.users import User


class Issue(GitHubCore):
    """The :class:`Issue <Issue>` object. It structures and handles the data
    returned via the `Issues <http://developer.github.com/v3/issues>`_ section
    of the GitHub API.

    Two issue instances can be checked like so::

        i1 == i2
        i1 != i2

    And is equivalent to::

        i1.id == i2.id
        i1.id != i2.id

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
        m = match('https://api.github\.com/repos/(\S+)/(\S+)/issues/\d+', self._api)
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

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return '<Issue [{r[0]}/{r[1]} #{n}]>'.format(r=self.repository,
                                                     n=self.number)

    def _update_(self, issue):
        self.__init__(issue, self._session)

    @requires_auth
    def add_labels(self, *args):
        """Add labels to this issue.

        :param str args: (required), names of the labels you wish to add
        :returns: list of :class:`Label`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._post(url, data=args), 200)
        return [Label(l, self) for l in json] if json else []

    @requires_auth
    def assign(self, login):
        """Assigns user ``login`` to this issue. This is a short cut for
        ``issue.edit``.

        :param str login: username of the person to assign this issue to
        :returns: bool
        """
        if not login:
            return False
        number = self.milestone.number if self.milestone else None
        labels = [str(l) for l in self.labels]
        return self.edit(self.title, self.body, login, self.state, number,
                         labels)

    @requires_auth
    def close(self):
        """Close this issue.

        :returns: bool
        """
        assignee = self.assignee.login if self.assignee else ''
        number = self.milestone.number if self.milestone else None
        labels = [str(l) for l in self.labels]
        return self.edit(self.title, self.body, assignee, 'closed',
                         number, labels)

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
            json = self._json(self._post(url, data={'body': body}),
                              201)
        return IssueComment(json, self) if json else None

    @requires_auth
    def edit(self, title=None, body=None, assignee=None, state=None,
             milestone=None, labels=None):
        """Edit this issue.

        :param str title: Title of the issue
        :param str body: markdown formatted body (description) of the issue
        :param str assignee: login name of user the issue should be assigned
            to
        :param str state: accepted values: ('open', 'closed')
        :param int milestone: the NUMBER (not title) of the milestone to
            assign this to [1]_
        :param list labels: list of labels to apply this to
        :returns: bool

        .. [1] Milestone numbering starts at 1, i.e. the first milestone you
               create is 1, the second is 2, etc.
        """
        json = None
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels}
        self._remove_none(data)
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

    def iter_events(self, number=-1):
        """Iterate over events associated with this issue only.

        :param int number: (optional), number of events to return. Default: -1
            returns all events available.
        :returns: generator of :class:`IssueEvent <IssueEvent>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, IssueEvent)

    @requires_auth
    def remove_label(self, name):
        """Removes label ``name`` from this issue.

        :param str name: (required), name of the label to remove
        :returns: bool
        """
        url = self._build_url('labels', name, base_url=self._api)
        # Docs say it should be a list of strings returned, practice says it
        # is just a 204/404 response. I'm tenatively changing this until I
        # hear back from Support.
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def remove_all_labels(self):
        """Remove all labels from this issue.

        :returns: an empty list if successful
        """
        # Can either send DELETE or [] to remove all labels
        return self.replace_labels([])

    @requires_auth
    def replace_labels(self, labels):
        """Replace all labels on this issue with ``labels``.

        :param list labels: label names
        :returns: bool
        """
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._put(url, data=dumps(labels)), 200)
        return [Label(l, self) for l in json] if json else []

    @requires_auth
    def reopen(self):
        """Re-open a closed issue.

        :returns: bool
        """
        assignee = self.assignee.login if self.assignee else ''
        number = self.milestone.number if self.milestone else None
        labels = [str(l) for l in self.labels]
        return self.edit(self.title, self.body, assignee, 'open',
                         number, labels)
