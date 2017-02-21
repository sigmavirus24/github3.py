# -*- coding: utf-8 -*-
"""
github3.projects
=============

This module contains all the classes relating to projects.
"""
from json import dumps

from . import models
from . import users
from .decorators import requires_auth


class Project(models.GitHubCore):
    """The :class:`Project <Project>` object.

    See http://developer.github.com/v3/projects/
    """

    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.inertia-preview+json',
    }

    def _update_attributes(self, project):
        self._api = self._get_attribute(project, 'url')

        #: The body of the project
        self.body = self._get_attribute(project, 'body')

        #: datetime object representing when the project was created
        self.created_at = self._strptime_attribute(project, 'created_at')

        #: The user who created this project
        self.creator = self._class_attribute(
            project, 'creator', users.ShortUser, self,
        )

        #: The unique ID of the project
        self.id = self._get_attribute(project, 'id')

        #: The name of this project
        self.name = self._get_attribute(project, 'name')

        #: The number of the project
        self.number = self._get_attribute(project, 'number')

        #: The owner repo or organisation of this project
        self.owner_url = self._get_attribute(project, 'owner_url')

        #: datetime object representing the last time the object was changed
        self.updated_at = self._strptime_attribute(project, 'updated_at')

    def _repr(self):
        return '<Project [#{0}]>'.format(self.id)

    @requires_auth
    def delete(self):
        """Delete this project.

        :returns: bool
        """
        return self._boolean(self._delete(
            self._api, headers=self.CUSTOM_HEADERS), 204, 404)

    @requires_auth
    def update(self, name=None, body=None):
        """Update this project.

        :param str name: (optional), name of the project
        :param str body: (optional), body of the project
        :returns: bool
        """
        data = {'name': name, 'body': body}
        json = None
        self._remove_none(data)

        if data:
            json = self._json(self._patch(
                self._api, data=dumps(data), headers=self.CUSTOM_HEADERS), 200)

        if json:
            self._update_attributes(json)
            return True
        return False
