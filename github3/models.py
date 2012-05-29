"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps


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
        self._bodyt = comment.get('body_text')
        self._bodyh = comment.get('body_html')
        self._user = User(comment.get('user'), self._session)
        self._created = self._strptime(comment.get('created_at'))
        self._updated = self._strptime(comment.get('updated_at'))

        self._api_url = comment.get('url')
        if comment.get('_links'):
            self._url = comment['_links'].get('html')
            self._pull = comment['_links'].get('pull_request')

        self._path = comment.get('path')
        self._pos = comment.get('position')
        self._cid = comment.get('commit_id')

    @property
    def body(self):
        return self._body

    @property
    def body_html(self):
        return self._bodyh

    @property
    def body_text(self):
        return self._bodyt

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
                self._update_(resp.json)
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


class BaseAccount(GitHubCore):
    def __init__(self, acct, session):
        super(BaseAccount, self).__init__(session)
        self._update_(acct)

    def __repr__(self):
        return '<BaseAccount [%s:%s]>' % (self._login, self._name)

    def _update_(self, acct):
        # Public information
        ## e.g. https://api.github.com/users/self._login
        self._type = None
        if acct.get('type'):
            self._type = acct.get('type')
        self._api_url = acct.get('url')

        self._avatar = acct.get('avatar_url')
        self._blog = acct.get('blog')
        self._company = acct.get('company')

        self._created = None
        if acct.get('created_at'):
            self._created = self._strptime(acct.get('created_at'))
        self._email = acct.get('email')

        ## The number of people following this acct
        self._followers = acct.get('followers')

        ## The number of people this acct follows
        self._following = acct.get('following')

        self._id = acct.get('id')
        self._location = acct.get('location')
        self._login = acct.get('login')

        ## e.g. first_name last_name
        self._name = acct.get('name')

        ## The number of public_repos
        self._public_repos = acct.get('public_repos')

        ## e.g. https://github.com/self._login
        self._url = acct.get('html_url')

        ## The number of private repos
        if self._type == 'Organization':
            self._private_repos = acct.get('private_repos')

        if self._type == 'User':
            self._bio = acct.get('bio')

            ## The number of people this acct folows
            self._grav_id = acct.get('gravatar_id')
            self._hire = acct.get('hireable')

            ## The number of public_gists
            self._public_gists = acct.get('public_gists')

            # Private information
            self._disk = acct.get('disk_usage')

            self._owned_private_repos = acct.get('owned_private_repos')
            self._private_gists = acct.get('total_private_gists')
            self._private_repos = acct.get('total_private_repos')

    @property
    def avatar(self):
        return self._avatar

    @property
    def bio(self):
        return self._bio

    @property
    def blog(self):
        return self._blog

    @property
    def company(self):
        return self._company

    @property
    def created_at(self):
        return self._created

    @property
    def email(self):
        return self._email

    @property
    def followers(self):
        return self._followers

    @property
    def following(self):
        return self._following

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    @property
    def location(self):
        return self._location

    @property
    def login(self):
        return self._login

    @property
    def name(self):
        return self._name

    @property
    def public_repos(self):
        return self._public_repos

class Error(object):
    def __init__(self, code, error):
        super(Error, self).__init__()
        self._code = code
        self._message = error.get('message')
        self._errors = []
        if code == 422:
            for e in error.get('errors'):
                self._errors.append(type(e.get('code'), (Error, ), e))

    def __repr__(self):
        return '<Error [%s]>' % (self._message or self._code)

    @property
    def code(self):
        return self._code

    @property
    def errors(self):
        return self._errors

    @property
    def message(self):
        return self._message
