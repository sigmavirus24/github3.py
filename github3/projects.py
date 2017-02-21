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

    def column(self, id):
        """Get a project column with the given ID.

        :param int id: (required), the column ID
        :returns: :class:`ProjectColumn <github3.projects.ProjectColumn>`
            or None
        """
        url = self._build_url(
            'projects', 'columns', str(id), base_url=self._github_url)
        json = self._json(self._get(url, headers=Project.CUSTOM_HEADERS), 200)
        return self._instance_or_null(ProjectColumn, json)

    def columns(self, number=-1, etag=None):
        """Iterate over the columns in this project.

        :param int number: (optional), number of columns to return. Default:
            -1 returns all available columns.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of
            :class:`ProjectColumn <github3.project.ProjectColumn>`
        """
        url = self._build_url(
            'projects', str(self.id), 'columns', base_url=self._github_url)
        return self._iter(
            int(number),
            url,
            ProjectColumn,
            headers=Project.CUSTOM_HEADERS,
            etag=etag
        )

    @requires_auth
    def create_column(self, name):
        """Create a column in this project.

        :param str name: (required), name of the column
        :returns: :class:`ProjectColumn <github3.projects.ProjectColumn>`
            or none
        """
        url = self._build_url('columns', base_url=self._api)
        json = None
        if name:
            json = self._json(self._post(
                url, data={'name': name}, headers=Project.CUSTOM_HEADERS), 201)
        return self._instance_or_null(ProjectColumn, json)

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


class ProjectColumn(models.GitHubCore):
    """The :class:`ProjectColumn <ProjectColumn>` object.

    See http://developer.github.com/v3/projects/columns/
    """

    def _update_attributes(self, project_column):
        #: datetime object representing the last time the object was created
        self.created_at = self._strptime_attribute(
            project_column, 'created_at')

        #: The ID of this column
        self.id = self._get_attribute(project_column, 'id')

        #: The name of this column
        self.name = self._get_attribute(project_column, 'name')

        #: The URL of this column's project
        self.project_url = self._get_attribute(project_column, 'project_url')

        #: datetime object representing the last time the object was changed
        self.updated_at = self._strptime_attribute(
            project_column, 'updated_at')

    def _repr(self):
        return '<ProjectColumn [#{0}]>'.format(self.id)

    @requires_auth
    def delete(self):
        """Delete this column.

        :returns: bool
        """
        url = self._build_url(
            'projects/columns', self.id, base_url=self._github_url)
        return self._boolean(self._delete(
            url, headers=Project.CUSTOM_HEADERS), 204, 404)

    @requires_auth
    def move(self, position):
        """Move this column.

        :param str position: (required), can be one of `first`, `last`,
            or `after:<column-id>`, where `<column-id>` is the id value
            of a column in the same project.
        :returns: bool
        """
        if not position:
            return False

        url = self._build_url(
            'projects/columns',
            self.id,
            'moves',
            base_url=self._github_url
        )
        data = {'position': position}
        return self._boolean(self._post(
            url, data=data, headers=Project.CUSTOM_HEADERS), 201, 404)

    @requires_auth
    def update(self, name=None):
        """Update this column.

        :param str name: (optional), name of the column
        :returns: bool
        """
        data = {'name': name}
        json = None
        self._remove_none(data)

        if data:
            url = self._build_url(
                'projects/columns', self.id, base_url=self._github_url)
            json = self._json(self._patch(
                url, data=dumps(data), headers=Project.CUSTOM_HEADERS), 200)

        if json:
            self._update_attributes(json)
            return True
        return False
