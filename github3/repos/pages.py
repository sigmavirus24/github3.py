# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..models import GitHubCore


class PagesInfo(GitHubCore):
    def _update_attributes(self, info):
        self._api = self._get_attribute(info, 'url')

        #: Status of the pages site, e.g., built
        self.status = self._get_attribute(info, 'status')

        #: CName used for the pages site
        self.cname = self._get_attribute(info, 'cname')

        #: Boolean indicating whether there is a custom 404 for the pages site
        self.custom_404 = self._get_attribute(info, 'custom_404')

    def _repr(self):
        info = self.cname or ''
        if info:
            info += '/'
        info += self.status or ''
        return '<Pages Info [{0}]>'.format(info)


class PagesBuild(GitHubCore):
    def _update_attributes(self, build):
        self._api = self._get_attribute(build, 'url')

        #: Status of the pages build, e.g., building
        self.status = self._get_attribute(build, 'status')

        #: Error dictionary containing the error message
        self.error = self._get_attribute(build, 'error')

        from .. import users
        #: :class:`User <github3.users.User>` representing who pushed the
        #: commit
        self.pusher = self._class_attribute(build, 'pusher', users.ShortUser)

        #: SHA of the commit that triggered the build
        self.commit = self._get_attribute(build, 'commit')

        #: Time the build took to finish
        self.duration = self._get_attribute(build, 'duration')

        #: Datetime the build was created
        self.created_at = self._strptime_attribute(build, 'created_at')

        #: Datetime the build was updated
        self.updated_at = self._strptime_attribute(build, 'updated_at')

    def _repr(self):
        return '<Pages Build [{0}/{1}]>'.format(self.commit, self.status)
