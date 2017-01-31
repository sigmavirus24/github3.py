# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import dumps
from re import match

from uritemplate import URITemplate

from .. import users

from ..decorators import requires_auth
from ..models import GitHubCore
from .comment import IssueComment, issue_comment_params
from .event import IssueEvent
from .label import Label
from .milestone import Milestone


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

    def _update_attributes(self, issue):
        self._api = self._get_attribute(issue, 'url', '')

        #: :class:`User <github3.users.User>` representing the user the issue
        #: was assigned to.
        self.assignee = self._class_attribute(
            issue, 'assignee', users.ShortUser, self)
        self.assignees = self._get_attribute(issue, 'assignees')
        if self.assignees:
            self.assignees = [
                users.ShortUser(assignee) for assignee in self.assignees
            ]

        #: Body (description) of the issue.
        self.body = self._get_attribute(issue, 'body')

        #: HTML formatted body of the issue.
        self.body_html = self._get_attribute(issue, 'body_html')

        #: Plain text formatted body of the issue.
        self.body_text = self._get_attribute(issue, 'body_text')

        # If an issue is still open, this field will be None
        #: datetime object representing when the issue was closed.
        self.closed_at = self._strptime_attribute(issue, 'closed_at')

        #: Number of comments on this issue.
        self.comments_count = self._get_attribute(issue, 'comments')

        #: Comments url (not a template)
        self.comments_url = self._get_attribute(issue, 'comments_url')

        #: datetime object representing when the issue was created.
        self.created_at = self._strptime_attribute(issue, 'created_at')

        #: Events url (not a template)
        self.events_url = self._get_attribute(issue, 'events_url')

        #: URL to view the issue at GitHub.
        self.html_url = self._get_attribute(issue, 'html_url')

        #: Unique ID for the issue.
        self.id = self._get_attribute(issue, 'id')

        #: Returns the list of :class:`Label <github3.issues.label.Label>`\ s
        #: on this issue.
        self.original_labels = self._get_attribute(issue, 'labels', [])
        if self.original_labels:
            self.original_labels = [
                Label(l, self) for l in self.original_labels
            ]

        #: Labels URL Template. Expand with ``name``
        self.labels_urlt = self._get_attribute(
            issue, 'labels_url', URITemplate
        )

        #: Locked status
        self.locked = self._get_attribute(issue, 'locked')

        #: :class:`Milestone <github3.issues.milestone.Milestone>` this
        #: issue was assigned to.
        self.milestone = self._class_attribute(
            issue, 'milestone', Milestone, self)

        #: Issue number (e.g. #15)
        self.number = self._get_attribute(issue, 'number')

        #: Dictionary URLs for the pull request (if they exist)
        self.pull_request_urls = self._get_attribute(issue, 'pull_request', {})

        #: Returns ('owner', 'repository') this issue was filed on.
        self.repository = None
        if self.html_url:
            m = match('https?://[\w\d\-\.\:]+/(\S+)/(\S+)/(?:issues|pull)/\d+',
                      self.html_url)
            self.repository = m.groups()

        #: State of the issue, e.g., open, closed
        self.state = self._get_attribute(issue, 'state')

        #: Title of the issue.
        self.title = self._get_attribute(issue, 'title')

        #: datetime object representing the last time the issue was updated.
        self.updated_at = self._strptime_attribute(issue, 'updated_at')

        #: :class:`User <github3.users.User>` who opened the issue.
        self.user = self._class_attribute(
            issue, 'user', users.ShortUser, self)

        #: :class:`User <github3.users.User>` who closed the issue.
        self.closed_by = self._class_attribute(
            issue, 'closed_by', users.ShortUser, self)

    def _repr(self):
        return '<Issue [{r[0]}/{r[1]} #{n}]>'.format(r=self.repository,
                                                     n=self.number)

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
    def assign(self, username):
        """Assigns user ``username`` to this issue. This is a short cut for
        ``issue.edit``.

        :param str username: username of the person to assign this issue to
        :returns: bool
        """
        if not username:
            return False
        number = self.milestone.number if self.milestone else None
        labels = [str(l) for l in self.original_labels]
        return self.edit(self.title, self.body, username, self.state, number,
                         labels)

    @requires_auth
    def close(self):
        """Close this issue.

        :returns: bool
        """
        assignee = self.assignee.login if self.assignee else ''
        number = self.milestone.number if self.milestone else None
        labels = [str(l) for l in self.original_labels]
        return self.edit(self.title, self.body, assignee, 'closed',
                         number, labels)

    def comment(self, id_num):
        """Get a single comment by its id.

        The catch here is that id is NOT a simple number to obtain. If
        you were to look at the comments on issue #15 in
        sigmavirus24/Todo.txt-python, the first comment's id is 4150787.

        :param int id_num: (required), comment id, see example above
        :returns: :class:`IssueComment <github3.issues.comment.IssueComment>`
        """
        json = None
        if int(id_num) > 0:  # Might as well check that it's positive
            owner, repo = self.repository
            url = self._build_url('repos', owner, repo, 'issues', 'comments',
                                  str(id_num))
            json = self._json(self._get(url), 200)
        return self._instance_or_null(IssueComment, json)

    def comments(self, number=-1, sort='', direction='', since=None):
        """Iterate over the comments on this issue.

        :param int number: (optional), number of comments to iterate over
            Default: -1 returns all comments
        :param str sort: accepted valuees: ('created', 'updated')
            api-default: created
        :param str direction: accepted values: ('asc', 'desc')
            Ignored without the sort parameter
        :param since: (optional), Only issues after this date will
            be returned. This can be a `datetime` or an ISO8601 formatted
            date string, e.g., 2012-05-20T23:10:27Z
        :type since: datetime or string
        :returns: iterator of
            :class:`IssueComment <github3.issues.comment.IssueComment>`\ s
        """
        url = self._build_url('comments', base_url=self._api)
        params = issue_comment_params(sort, direction, since)
        return self._iter(int(number), url, IssueComment, params)

    @requires_auth
    def create_comment(self, body):
        """Create a comment on this issue.

        :param str body: (required), comment body
        :returns: :class:`IssueComment <github3.issues.comment.IssueComment>`
        """
        json = None
        if body:
            url = self._build_url('comments', base_url=self._api)
            json = self._json(self._post(url, data={'body': body}),
                              201)
        return self._instance_or_null(IssueComment, json)

    @requires_auth
    def edit(self, title=None, body=None, assignee=None, state=None,
             milestone=None, labels=None, assignees=None):
        """Edit this issue.

        :param str title: Title of the issue
        :param str body: markdown formatted body (description) of the issue
        :param str assignee: login name of user the issue should be assigned
            to
        :param str state: accepted values: ('open', 'closed')
        :param int milestone: the NUMBER (not title) of the milestone to
            assign this to [1]_, or 0 to remove the milestone
        :param list labels: list of labels to apply this to
        :param assignees: (optional), login of the users to assign the
            issue to
        :type assignees: list of strings
        :returns: bool

        .. [1] Milestone numbering starts at 1, i.e. the first milestone you
               create is 1, the second is 2, etc.
        """
        json = None
        data = {'title': title, 'body': body, 'assignee': assignee,
                'state': state, 'milestone': milestone, 'labels': labels,
                'assignees': assignees}
        self._remove_none(data)
        if data:
            if 'milestone' in data and data['milestone'] == 0:
                data['milestone'] = None
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False

    def events(self, number=-1):
        """Iterate over events associated with this issue only.

        :param int number: (optional), number of events to return. Default: -1
            returns all events available.
        :returns: generator of
            :class:`IssueEvent <github3.issues.event.IssueEvent>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, IssueEvent)

    def is_closed(self):
        """Checks if the issue is closed.

        :returns: bool
        """
        if self.closed_at or (self.state == 'closed'):
            return True
        return False

    def labels(self, number=-1, etag=None):
        """Iterate over the labels associated with this issue.

        :param int number: (optional), number of labels to return. Default: -1
            returns all labels applied to this issue.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Label <github3.issues.label.Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        return self._iter(int(number), url, Label, etag=etag)

    @requires_auth
    def lock(self):
        """Lock an issue.

        :returns: bool
        """

        url = self._build_url('lock', base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    def pull_request(self):
        """Retrieve the pull request associated with this issue.

        :returns: :class:`~github3.pulls.PullRequest`
        """
        from .. import pulls
        json = None
        pull_request_url = self.pull_request_urls.get('url')
        if pull_request_url:
            json = self._json(self._get(pull_request_url), 200)
        return self._instance_or_null(pulls.PullRequest, json)

    @requires_auth
    def remove_label(self, name):
        """Removes label ``name`` from this issue.

        :param str name: (required), name of the label to remove
        :returns: list of :class:`Label`
        """
        url = self._build_url('labels', name, base_url=self._api)
        json = self._json(self._delete(url), 200, 404)
        labels = [Label(label, self) for label in json] if json else []
        return labels

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
        :returns: list of :class:`Label`
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
        labels = [str(l) for l in self.original_labels]
        return self.edit(self.title, self.body, assignee, 'open',
                         number, labels)

    @requires_auth
    def unlock(self):
        """Unlock an issue.

        :returns: bool
        """

        url = self._build_url('lock', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)
