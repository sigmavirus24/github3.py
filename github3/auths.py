"""
github3.auths
=============

This module contains the Authorization object.

"""

from github3.decorators import requires_basic_auth
from github3.models import GitHubCore
from json import dumps


class Authorization(GitHubCore):
    """The :class:`Authorization <Authorization>` object."""
    def __init__(self, auth, session=None):
        super(Authorization, self).__init__(auth, session)
        #: Details about the application (name, url)
        self.app = auth.get('app', {})
        #: Returns the Authorization token
        self.token = auth.get('token', '')
        #: App name
        self.name = self.app.get('name', '')
        #: URL about the note
        self.note_url = auth.get('note_url') or ''
        #: Note about the authorization
        self.note = auth.get('note') or ''
        #: List of scopes this applies to
        self.scopes = auth.get('scopes', [])
        #: Unique id of the authorization
        self.id = auth.get('id', 0)
        self._api = self._build_url('authorizations', str(self.id))
        #: datetime object representing when the authorization was created.
        self.created_at = None
        if auth.get('created_at'):
            self.created_at = self._strptime(auth.get('created_at'))
        #: datetime object representing when the authorization was created.
        self.updated_at = None
        if auth.get('updated_at'):
            self.updated_at = self._strptime(auth.get('updated_at'))

    def __repr__(self):
        return '<Authorization [{0}]>'.format(self.name)

    def _update_(self, auth):
        self.__init__(auth, self._session)

    @requires_basic_auth
    def delete(self):
        """delete this authorization"""
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_basic_auth
    def update(self, scopes=[], add_scopes=[], rm_scopes=[], note='',
            note_url=''):
        """Update this authorization.

        :param scopes: (optional), replaces the authorization scopes with these
        :type scopes: list
        :param add_scopes: (optional), scopes to be added
        :type add_scopes: list
        :param rm_scopes: (optional), scopes to be removed
        :type rm_scopes: list
        :param note: (optional), new note about authorization
        :type note: str
        :param note_url: (optional), new note URL about this authorization
        :type note_url: str
        :returns: bool
        """
        success = False
        if scopes:
            d = dumps({'scopes': scopes})
            json = self._json(self._post(self._api, data=d), 200)
            self._update_(json)
            success = True
        if add_scopes:
            d = dumps({'add_scopes': add_scopes})
            json = self._json(self._post(self._api, data=d), 200)
            self._update_(json)
            success = True
        if rm_scopes:
            d = dumps({'remove_scopes': rm_scopes})
            json = self._json(self._post(self._api, data=d), 200)
            self._update_(json)
            success = True
        if note or note_url:
            d = dumps({'note': note, 'note_url': note_url})
            json = self._json(self._post(self._api, data=d), 200)
            self._update_(json)
            success = True
        return success
