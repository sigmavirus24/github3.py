# -*- coding: utf-8 -*-
"""
github3.auths
=============

This module contains the Authorization object.

"""
from __future__ import unicode_literals

from .decorators import requires_basic_auth
from .models import GitHubCore


class Authorization(GitHubCore):

    """The :class:`Authorization <Authorization>` object.

    Two authorization instances can be checked like so::

        a1 == a2
        a1 != a2

    And is equivalent to::

        a1.id == a2.id
        a1.id != a2.id

    See also: http://developer.github.com/v3/oauth/#oauth-authorizations-api

    """

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
        self.created_at = self._strptime(auth.get('created_at'))
        #: datetime object representing when the authorization was updated.
        self.updated_at = self._strptime(auth.get('updated_at'))

    def _repr(self):
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

        :param list scopes: (optional), replaces the authorization scopes with
            these
        :param list add_scopes: (optional), scopes to be added
        :param list rm_scopes: (optional), scopes to be removed
        :param str note: (optional), new note about authorization
        :param str note_url: (optional), new note URL about this authorization
        :returns: bool

        """
        success = False
        json = None
        if scopes:
            d = {'scopes': scopes}
            json = self._json(self._post(self._api, data=d), 200)
        if add_scopes:
            d = {'add_scopes': add_scopes}
            json = self._json(self._post(self._api, data=d), 200)
        if rm_scopes:
            d = {'remove_scopes': rm_scopes}
            json = self._json(self._post(self._api, data=d), 200)
        if note or note_url:
            d = {'note': note, 'note_url': note_url}
            json = self._json(self._post(self._api, data=d), 200)

        if json:
            self._update_(json)
            success = True

        return success
