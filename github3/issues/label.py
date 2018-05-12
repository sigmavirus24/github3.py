# -*- coding: utf-8 -*-
"""Module containing the logic for labels."""
from __future__ import unicode_literals

from json import dumps
from ..decorators import requires_auth
from ..models import GitHubCore


class Label(GitHubCore):
    """A representation of a label object defined on a repository.

    See also: http://developer.github.com/v3/issues/labels/

    This object has the following attributes::

    .. attribute:: color

        The hexadecimeal representation of the background color of this label.

    .. attribute:: name

        The name (display label) for this label.
    """

    def _update_attributes(self, label):
        self._api = label['url']
        self.color = label['color']
        self.name = label['name']
        self.description = label.get('description')
        self._uniq = self._api

    def _repr(self):
        return '<Label [{0}]>'.format(self)

    def __str__(self):
        return self.name

    @requires_auth
    def delete(self):
        """Delete this label.

        :returns:
            True if successfully deleted, False otherwise
        :rtype:
            bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, name, color):
        """Update this label.

        :param str name:
            (required), new name of the label
        :param str color:
            (required), color code, e.g., 626262, no leading '#'
        :returns:
            True if successfully updated, False otherwise
        :rtype:
            bool
        """
        json = None

        if name and color:
            if color[0] == '#':
                color = color[1:]
            json = self._json(self._patch(self._api, data=dumps({
                'name': name, 'color': color})), 200)

        if json:
            self._update_attributes(json)
            return True

        return False
