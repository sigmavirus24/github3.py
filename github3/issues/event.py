from github3.models import GitHubCore


class IssueEvent(GitHubCore):
    """The :class:`IssueEvent <IssueEvent>` object. This specifically deals
    with events described in the
    `Issues\>Events <http://developer.github.com/v3/issues/events>`_ section of
    the GitHub API.

    Two event instances can be checked like so::

        e1 == e2
        e1 != e2

    And is equivalent to::

        e1.commit_id == e2.commit_id
        e1.commit_id != e2.commit_id

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

        #: :class:`Issue <github3.issue.Issue>` where this comment was made.
        self.issue = issue
        if event.get('issue'):
            from github3.issues import Issue
            self.issue = Issue(event.get('issue'), self)

        #: Number of comments
        self.comments = event.get('comments', 0)

        #: datetime object representing when the event was created.
        self.created_at = self._strptime(event.get('created_at'))

        #: Dictionary of links for the pull request
        self.pull_request = event.get('pull_request', {})

    def __eq__(self, other):
        return self.commit_id == other.commit_id

    def __ne__(self, other):
        return self.commit_id != other.commit_id

    def __repr__(self):
        return '<Issue Event [#{0} - {1}]>'.format(
            self.issue.number, self.event
        )
