"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps
from .compat import loads


class GitHubCore(object):
    """A basic class for the other classes."""
    def __init__(self, session=None):
        self._session = session
        self._github_url = 'https://api.github.com'
        self._time_format = '%Y-%m-%dT%H:%M:%SZ'

    def __repr__(self):
        return '<github3-core at 0x%x>' % id(self)

    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def _get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def _patch(self, url, data=None, **kwargs):
        return self._session.patch(url, data, **kwargs)

    def _post(self, url, data=None, **kwargs):
        return self._session.post(url, data, **kwargs)

    def _put(self, url, data=None, **kwargs):
        kwargs.update(headers={'Content-Length': '0'})
        return self._session.put(url, data, **kwargs)

    def _strptime(self, time_str):
        return datetime.strptime(time_str, self._time_format)


class BaseComment(GitHubCore):
    """A basic class for Gist, Issue and Pull Request Comments."""
    def __init__(self, comment, session):
        super(BaseComment, self).__init__(session)
        self._update_(comment)

    def __repr__(self):
        return '<github3-comment at 0x%x>' % id(self)

    def _update_(self, comment):
        self._id = comment.get('id')
        self._body = comment.get('body')
        self._user = User(comment.get('user'), self._session)
        self._created = self._strptime(comment.get('created_at'))
        self._updated = self._strptime(comment.get('updated_at'))

        self._api_url = comment.get('url')
        if comment.get('_links'):
            self._url = comment['_links'].get('html')
            self._pull = comment['_links'].get('pull_request')

        self._path = comment.get('path')
        self._pos = comment.get('position')
        self._cid = comment.get('comment_id')

    @property
    def body(self):
        return self._body

    @property
    def created_at(self):
        return self._created

    def delete(self):
        """Delete this comment."""
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    def edit(self, body):
        """Edit this comment."""
        if body:
            resp = self._patch(self._api_url, dumps({'body': body}))
            if resp.status_code == 200:
                self._update_(loads(resp.content))
                return True
        return False

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user


class BaseEvent(GitHubCore):
    def __init__(self, event, session):
        super(BaseEvent, self).__init__(session)
        # Guaranteed to exist
        self._actor = User(event.get('actor'), self._session)
        self._created = self._strptime(event.get('created_at'))

    def __repr__(self):
        return '<github3-event at 0x%x>' % id(self)

    @property
    def actor(self):
        return self._actor

    @property
    def created_at(self):
        return self._created
