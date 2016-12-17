# -*- coding: utf-8 -*-
"""
github3.auths
=============

This module contains the Authorization object.

"""
from __future__ import unicode_literals

import base64

from . import decorators
from . import models


class Authorization(models.GitHubCore):

    """The :class:`Authorization <Authorization>` object.

    Two authorization instances can be checked like so::

        a1 == a2
        a1 != a2

    And is equivalent to::

        a1.id == a2.id
        a1.id != a2.id

    See also: http://developer.github.com/v3/oauth/#oauth-authorizations-api

    """

    CUSTOM_HEADERS = {'Accept': 'application/vnd.github.mirage-preview+json'}

    def _update_attributes(self, auth):
        self._api = auth.get('url')
        #: Details about the application (name, url)
        self.app = auth.get('app', {})
        #: **DEPRECATED** Returns the Authorization token
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
        #: datetime object representing when the authorization was created.
        self.created_at = self._strptime(auth.get('created_at'))
        #: datetime object representing when the authorization was updated.
        self.updated_at = self._strptime(auth.get('updated_at'))
        #: Last eight characters of the associated OAuth token
        self.token_last_eight = auth.get('token_last_eight')
        #: base64-encoded of the SHA-256 digest of the token
        self.hashed_token = auth.get('hashed_token')
        #: SHA-256 digest of the token (derived from ``hashed_token``)
        self.sha256_hashed_token = None
        if self.hashed_token:
            self.sha256_hashed_token = base64.b64decode(self.hashed_token)
        #: A string that distinguishes the new authorization from others for
        #: the same client ID and user
        self.fingerprint = auth.get('fingerprint')

    def _repr(self):
        return '<Authorization [{0}]>'.format(self.name)

    def _update(self, scopes_data, note, note_url):
        """Helper for add_scopes, replace_scopes, remove_scopes."""
        if note is not None:
            scopes_data['note'] = note
        if note_url is not None:
            scopes_data['note_url'] = note_url
        json = self._json(self._post(self._api, data=scopes_data), 200)

        if json:
            self._update_attributes(json)
            return True

        return False

    @decorators.requires_basic_auth
    def add_scopes(self, scopes, note=None, note_url=None):
        """Adds the scopes to this authorization.

        .. versionadded:: 1.0

        :param list scopes: Adds these scopes to the ones present on this
            authorization
        :param str note: (optional), Note about the authorization
        :param str note_url: (optional), URL to link to when the user views
            the authorization
        :returns: True if successful, False otherwise
        :rtype: bool
        """
        return self._update({'add_scopes': scopes}, note, note_url)

    @decorators.requires_basic_auth
    def delete(self):
        """Delete this authorization."""
        return self._boolean(self._delete(self._api), 204, 404)

    @decorators.requires_basic_auth
    def remove_scopes(self, scopes, note=None, note_url=None):
        """Remove the scopes from this authorization.

        .. versionadded:: 1.0

        :param list scopes: Remove these scopes from the ones present on this
            authorization
        :param str note: (optional), Note about the authorization
        :param str note_url: (optional), URL to link to when the user views
            the authorization
        :returns: True if successful, False otherwise
        :rtype: bool
        """
        return self._update({'rm_scopes': scopes}, note, note_url)

    @decorators.requires_basic_auth
    def replace_scopes(self, scopes, note=None, note_url=None):
        """Replace the scopes on this authorization.

        .. versionadded:: 1.0

        :param list scopes: Use these scopes instead of the previous list
        :param str note: (optional), Note about the authorization
        :param str note_url: (optional), URL to link to when the user views
            the authorization
        :returns: True if successful, False otherwise
        :rtype: bool
        """
        return self._update({'scopes': scopes}, note, note_url)
