# -*- coding: utf-8 -*-
"""
github3.repos.hook
==================

This module contains only the Hook object for GitHub's Hook API.

"""

from json import dumps
from github3.decorators import requires_auth
from github3.models import GitHubCore


class Hook(GitHubCore):
    """The :class:`Hook <Hook>` object. This handles the information returned
    by GitHub about hooks set on a repository.

    Two hook instances can be checked like so::

        h1 == h2
        h1 != h2

    And is equivalent to::

        h1.id == h2.id
        h1.id != h2.id

    See also: http://developer.github.com/v3/repos/hooks/
    """
    def __init__(self, hook, session=None):
        super(Hook, self).__init__(hook, session)
        self._api = hook.get('url', '')
        #: datetime object representing when this hook was last updated.
        self.updated_at = None
        if hook.get('updated_at'):
            self.updated_at = self._strptime(hook.get('updated_at'))
        #: datetime object representing the date the hook was created.
        self.created_at = self._strptime(hook.get('created_at'))
        #: The name of the hook.
        self.name = hook.get('name')
        #: Events which trigger the hook.
        self.events = hook.get('events')
        #: Whether or not this Hook is marked as active on GitHub
        self.active = hook.get('active')
        #: Dictionary containing the configuration for the Hook.
        self.config = hook.get('config')
        #: Unique id of the hook.
        self.id = hook.get('id')

    def __repr__(self):
        return '<Hook [{0}]>'.format(self.name)

    def _update_(self, hook):
        self.__init__(hook, self._session)

    @requires_auth
    def delete(self):
        """Delete this hook.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def delete_subscription(self):
        """Delete the user's subscription to this repository.

        :returns: bool
        """
        url = self._build_url('subscription', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def edit(self, config={}, events=[], add_events=[], rm_events=[],
             active=True):
        """Edit this hook.

        :param dict config: (optional), key-value pairs of settings for this
            hook
        :param list events: (optional), which events should this be triggered
            for
        :param list add_events: (optional), events to be added to the list of
           events that this hook triggers for
        :param list rm_events: (optional), events to be remvoed from the list
            of events that this hook triggers for
        :param bool active: (optional), should this event be active
        :returns: bool
        """
        data = {'config': config, 'active': active}
        if events:
            data['events'] = events

        if add_events:
            data['add_events'] = add_events

        if rm_events:
            data['remove_events'] = rm_events

        json = self._json(self._patch(self._api, data=dumps(data)), 200)

        if json:
            self._update_(json)
            return True

        return False

    @requires_auth
    def test(self):
        """Test this hook

        :returns: bool
        """
        url = self._build_url('tests', base_url=self._api)
        return self._boolean(self._post(url), 204, 404)
