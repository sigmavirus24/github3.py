"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .models import GitHubCore


class Event(GitHubCore):
    """The :class:`Event <Event>` object. It structures and handles the data
    returned by via the `Events <http://developer.github.com/v3/events>`_
    section of the GitHub API.
    """
    def __init__(self, event, session=None):
        super(Event, self).__init__(event, session)
        from .users import User
        from .orgs import Organization
        self._created = self._strptime(event.get('created_at'))
        self._type = event.get('type')
        self._public = event.get('public')
        self._repo = event.get('repo', {})
        self._actor = event.get('actor', {})
        if self._actor:
            self._actor = User(self._actor, self._session)
        self._id = event.get('id')
        handler = _payload_handlers[self._type]
        self._payload = handler(event.get('payload'))
        self._org = event.get('org', {})
        if self._org:
            self._org = Organization(self._org, self)

    def __repr__(self):
        return '<Event [{0}]>'.format(self._type[:-5])

    @property
    def actor(self):
        """:class:`User <github3.user.User>` object representing the actor."""
        return self._actor

    @property
    def created_at(self):
        """datetime object representing when the event was created."""
        return self._created

    @property
    def id(self):
        """Unique id of the event"""
        return self._id

    @staticmethod
    def list_types():
        """List all possible types of Events"""
        return sorted(_payload_handlers.keys())

    @property
    def org(self):
        """:class:`Organization <github3.org.Organization>` object if actor
        was an org."""
        return self._org

    @property
    def payload(self):
        """Dictionary with the payload. Payload structure is defined by type_.

        .. _type: http://developer.github.com/v3/events/types
        """
        return self._payload

    def is_public(self):
        """Indicates whether the Event is public or not.

        :returns: bool -- True if event is pubic, False otherwise
        """
        return self._public

    @property
    def repo(self):
        """Return ``tuple(owner, repository_name)``"""
        return tuple(self._repo['name'].split('/'))

    @property
    def type(self):
        """Event type"""
        return self._type


def _commitcomment(payload):
    from .repos import RepoComment
    if payload.get('comment'):
        payload['comment'] = RepoComment(payload['comment'], None)
    return payload


def _download(payload):
    from .repos import Download
    if payload.get('download'):
        payload['download'] = Download(payload['download'], None)
    return payload


def _follow(payload):
    from .users import User
    if payload.get('target'):
        payload['target'] = User(payload['target'], None)
    return payload


def _forkev(payload):
    from .repos import Repository
    if payload.get('forkee'):
        payload['forkee'] = Repository(payload['forkee'], None)
    return payload


def _gist(payload):
    from .gists import Gist
    if payload.get('gist'):
        payload['gist'] = Gist(payload['gist'], None)
    return payload


def _issuecomm(payload):
    from .issues import Issue, IssueComment
    if payload.get('issue'):
        payload['issue'] = Issue(payload['issue'], None)
    if payload.get('comment'):
        payload['comment'] = IssueComment(payload['comment'], None)
    return payload


def _issueevent(payload):
    from .issues import Issue
    if payload.get('issue'):
        payload['issue'] = Issue(payload['issue'], None)
    return payload


def _member(payload):
    from .users import User
    if payload.get('member'):
        payload['member'] = User(payload['member'], None)
    return payload


def _pullreqev(payload):
    from .pulls import PullRequest
    if payload.get('pull_request'):
        payload['pull_request'] = PullRequest(payload['pull_request'], None)
    return payload


def _pullreqcomm(payload):
    from .pulls import ReviewComment
    if payload.get('comment'):
        payload['comment'] = ReviewComment(payload['comment'], None)
    return payload


def _team(payload):
    from .orgs import Team
    from .repos import Repository
    from .users import User
    if payload.get('team'):
        payload['team'] = Team(payload['team'], None)
    if payload.get('repo'):
        payload['repo'] = Repository(payload['repo'], None)
    if payload.get('user'):
        payload['user'] = User(payload['user'], None)
    return payload


_payload_handlers = {
        'CommitCommentEvent': _commitcomment,
        'CreateEvent': lambda x: x,
        'DeleteEvent': lambda x: x,
        'DownloadEvent': _download,
        'FollowEvent': _follow,
        'ForkEvent': _forkev,
        'ForkApplyEvent': lambda x: x,
        'GistEvent': _gist,
        'GollumEvent': lambda x: x,
        'IssueCommentEvent': _issuecomm,
        'IssuesEvent': _issueevent,
        'MemberEvent': _member,
        'PublicEvent': lambda x: '',
        'PullRequestEvent': _pullreqev,
        'PullRequestReviewCommentEvent': _pullreqcomm,
        'PushEvent': lambda x: x,
        'TeamAddEvent': _team,
        'WatchEvent': lambda x: x,
        }
