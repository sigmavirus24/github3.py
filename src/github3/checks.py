# -*- coding: utf-8 -*-
"""This module contains all the classes relating to Checks."""
from __future__ import unicode_literals

from json import dumps

from . import models
from .decorators import requires_auth


class CheckSuite(models.GitHubCore):
    """The :class:`CheckSuite <CheckSuite>` object.

    .. versionadded:: 1.2.0

    Please see GitHub's `CheckSuite Documentation`_ for more information.

    .. attribute:: status

        The status of the Check Suite

    .. attribute:: conclusion

        The highest priority check run conclusion. If it has not completed this
        will be None

    .. attribute:: head_sha

        The sha of the commit at the head of the branch checked

    .. attribute:: head_branch

        The branch checked

    .. attribute:: before

        The sha of the target branch before the change

    .. attribute:: after

        The sha of the target branch after the change is applied

    .. attribute:: repository

        A representation of the repository the suite belongs to as
        :class:`~github3.repos.repo.ShortRepository`.

    .. attribute:: pull_requests

        A list of representations of the pull requests the suite belongs to as
        :class:`~github3.pulls.ShortPullRequest`. This may be empty.

    .. attribute:: id

        The unique GitHub assigned numerical id of this check suite.

    .. CheckSuite Documentation:
        http://developer.github.com/v3/checks/suites/
    """

    class_name = 'CheckSuite'
    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.antiope-preview+json'
    }

    def _update_attributes(self, suite):
        # Import here, because a toplevel import causes an import loop
        from . import pulls
        from .repos import ShortRepository
        self._api = suite['url']
        # self.base = Base(pull['base'], self)
        self.status = suite['status']
        self.conclusion = suite['conclusion']
        self.head_branch = suite['head_branch']
        self.head_sha = suite['head_sha']
        self.before = suite['before']
        self.after = suite['after']
        pull_requests = suite.get('pull_requests', [])
        self.pull_requests = [
            pulls.ShortPullRequest(p, self) for p in pull_requests
        ]
        self.repository = ShortRepository(suite['repository'], self)
        self.id = suite['id']

    def _repr(self):
        return '<{0} [{1}]>'.format(self.class_name, self.id)
        # FIXME(omgjlk): This could be more descriptive perhaps

    @requires_auth
    def rerequest(self):
        """Rerequest the check suite.

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """

        url = self._build_url('rerequest', base_url=self._api)
        return self._boolean(self._post(
            url, headers=CheckSuite.CUSTOM_HEADERS), 201, 404)

    @requires_auth
    def check_runs(self):
        """Retrieve the check runs for this suite.

        :returns:
            the check runs for this commit
        :rtype:
            :class:`~github3.checks.CheckRun`
        """
        url = self._build_url('check-runs', base_url=self._api)
        return self._iter(-1, url, CheckRun)


class CheckRun(models.GitHubCore):
    """The :class:`CheckRun <CheckRun>` object.

    .. versionadded:: 1.2.0

    Please see GitHub's `CheckRun Documentation`_ for more information.

    .. attribute:: status

        The current status of the check.

    .. attribute:: conclusion

        The final conclusion of the check. If the run has not concluded
        this will be None.

    .. attribute:: head_sha

        The sha of the commit at the head of the branch checked.

    .. attribute:: name

        The name of the check.

    .. attribute:: started_at

        A :class:`~datetime.datetime` object representing the date and time
        when this check run started.

    .. attribute:: completed_at

        A :class:`~datetime.datetime` object representing the date and time
        when this check run completed. If this run is not completed it will
        be ``None``.

    .. attribute:: pull_requests

        A list of representations of the pull requests the check run belongs to
        as :class:`~github3.pulls.ShortPullRequest` (this may be empty).

    .. attribute:: id

        The unique GitHub assigned numerical id of this check run.

    .. attribute:: external_id

        A reference for the run on the integrator's system. This may be None.

    .. attribute:: html_url

        The URL one would use to view this check run in the browser.

    .. attribute:: check_suite

        The ID of the check suite this run belongs to.

    .. attribute:: output

        A :class:`~github3.checks.CheckRunOutput` representing the output
        of this check run. (TODO: Implement this object)

    .. attribute:: app

        A :class:`~github3.apps.App` representing the App
        this run belongs to. (TODO: Implement this)

    .. CheckRun Documentation:
        http://developer.github.com/v3/checks/runs/
    """

    class_name = 'CheckRun'
    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.antiope-preview+json'
    }

    def _update_attributes(self, run):
        # Import here, because a toplevel import causes an import loop
        from . import pulls
        self._api = run['url']
        self.html_url = run['html_url']
        self.status = run['status']
        self.conclusion = run['conclusion']
        self.started_at = self._strptime(run['created_at'])
        self.completed_at = self._strptime(run['completed_at'])
        self.head_sha = run['head_sha']
        self.name = run['name']
        pull_requests = run.get('pull_requests', [])
        self.pull_requests = [
            pulls.ShortPullRequest(p, self) for p in pull_requests
        ]
        self.id = run['id']
        self.external_id = run['external_id']
        # self.app = app.App(run['app'], self)
        self.app = run['app']  # TODO: turn into an object
        self.check_suite = run['check_suite']['id']
        # self.output = CheckRunOutput(run['output'], self)
        self.output = run['output']  # TODO: turn into an object

    def _repr(self):
        return '<{s.class_name} [{s.name}:{s.status}]>'.format(s=self)

    @requires_auth
    def update(self, name=None, details_url=None, external_id=None,
               started_at=None, status=None, conclusion=None,
               completed_at=None, output=None, actions=None):
        """Update this check run.

        All parameters are optional.

        :param str name:
            (optional), new name of the check
        :param str details_url:
            (optional), The URL of the integrator's site that has the full
            details of the check
        :param str external_id:
            (optional), A reference for the run on the integrator's system
        :param str started_at:
            (optional), ISO 8601 time format: YYYY-MM-DDTHH:MM:SSZ
        :param str status:
            (optional), ('queued', 'in_progress', 'completed')
        :param str conclusion:
            (optional), Required if you provide 'completed_at', or a
            'status' of 'completed'. The final conclusion of the check.
            ('success', 'failure', 'neutral', 'cancelled', 'timed_out',
            'action_required')
        :param str completed_at:
            (optional), Required if you provide 'conclusion'. ISO 8601 time
            format: YYYY-MM-DDTHH:MM:SSZ
        :param dict output:
            (optional), key-value pairs representing the output. Format:
            {'title': 'string', 'summary', 'text, can be markdown', 'text':
            'text, can be markdown', 'annotations': [{}], 'images': [{}]}
        :param array actions:
            (optiona), array of action objects. Object format is:
            {'label': 'text', 'description', 'text', 'identifier', 'text'}
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """

        # TODO: Clean output dict, actions array. Need a deep recursive clean
        data = {'name': name, 'details_url': details_url, 'external_id':
                external_id, 'started_at': started_at, 'status': status,
                'conclusion': conclusion, 'completed_at': completed_at,
                'output': output, 'actions': actions}
        self._remove_none(data)
        json = None

        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False

    @requires_auth
    def rerequest(self):
        """Rerequest the check suite.

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """

        url = self._build_url('rerequest', base_url=self._api)
        return self._boolean(self._post(
            url, headers=CheckSuite.CUSTOM_HEADERS), 201, 404)
