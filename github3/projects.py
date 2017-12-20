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
        self._api = project['url']

        #: The body of the project
        self.body = project['body']

        #: datetime object representing when the project was created
        self.created_at = self._strptime(project['created_at'])

        #: The user who created this project
        self.creator = users.ShortUser(project['creator'], self)

        #: The unique ID of the project
        self.id = project['id']

        #: The name of this project
        self.name = project['name']

        #: The number of the project
        self.number = project['number']

        #: The owner repo or organisation of this project
        self.owner_url = project['owner_url']

        #: datetime object representing the last time the object was changed
        self.updated_at = self._strptime(project['updated_at'])

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
        self.created_at = self._strptime(project_column['created_at'])

        #: The ID of this column
        self.id = project_column['id']

        #: The name of this column
        self.name = project_column['name']

        #: The URL of this column's project
        self.project_url = project_column['project_url']

        #: datetime object representing the last time the object was changed
        self.updated_at = self._strptime(project_column['updated_at'])

    def _repr(self):
        return '<ProjectColumn [#{0}]>'.format(self.id)

    def card(self, id):
        """Get a project card with the given ID.

        :param int id: (required), the card ID
        :returns: :class:`ProjectCard <github3.projects.ProjectCard>` or None
        """
        url = self._build_url(
            'projects/columns/cards', str(id), base_url=self._github_url)
        json = self._json(self._get(url, headers=Project.CUSTOM_HEADERS), 200)
        return self._instance_or_null(ProjectCard, json)

    def cards(self, number=-1, etag=None):
        """Iterate over the cards in this column.

        :param int number: (optional), number of cards to return. Default:
            -1 returns all available cards.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of
            :class:`ProjectCard <github3.project.ProjectCard>`
        """
        url = self._build_url(
            'projects/columns',
            str(self.id),
            'cards',
            base_url=self._github_url
        )
        return self._iter(
            int(number),
            url,
            ProjectCard,
            headers=Project.CUSTOM_HEADERS,
            etag=etag
        )

    @requires_auth
    def create_card_with_content_id(self, content_id, content_type):
        """Create a content card in this project column.

        :param int content_id: (required), the ID of the content
        :param str content_type: (required), the type of the content
        :returns: :class:`ProjectCard <github3.projects.ProjectCard>` or none
        """
        if not content_id or not content_type:
            return None

        url = self._build_url(
            'projects/columns',
            str(self.id),
            'cards',
            base_url=self._github_url
        )
        json = None
        data = {'content_id': content_id, 'content_type': content_type}
        json = self._json(self._post(
            url, data=data, headers=Project.CUSTOM_HEADERS), 201)
        return self._instance_or_null(ProjectCard, json)

    @requires_auth
    def create_card_with_issue(self, issue):
        """Create a card in this project column linked with an Issue.

        :param :class:`Issue <github3.issues.Issue>`: (required), an issue
            with which to link the card. Can also be
            :class:`ShortIssue <github3.issues.ShortIssue>`.
        :returns: :class:`ProjectCard <github3.projects.ProjectCard>` or none
        """
        if not issue:
            return None
        return self.create_card_with_content_id(issue.id, 'Issue')

    @requires_auth
    def create_card_with_note(self, note):
        """Create a note card in this project column.

        :param str note: (required), the note content
        :returns: :class:`ProjectCard <github3.projects.ProjectCard>` or none
        """
        url = self._build_url(
            'projects/columns',
            str(self.id),
            'cards',
            base_url=self._github_url
        )
        json = None
        if note:
            json = self._json(self._post(
                url, data={'note': note}, headers=Project.CUSTOM_HEADERS), 201)
        return self._instance_or_null(ProjectCard, json)

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


class ProjectCard(models.GitHubCore):
    """The :class:`ProjectCard <ProjectCard>` object.

    See http://developer.github.com/v3/projects/cards/
    """

    def _update_attributes(self, project_card):
        #: The URL of this card's parent column
        self.column_url = project_card['column_url']

        #: The URL of this card's associated content
        self.content_url = project_card.get('content_url')

        #: datetime object representing the last time the object was created
        self.created_at = project_card['created_at']

        #: The ID of this card
        self.id = project_card['id']

        #: The note attached to the card
        self.note = project_card['note']

        #: datetime object representing the last time the object was changed
        self.updated_at = project_card['updated_at']

    def _repr(self):
        return '<ProjectCard [#{0}]>'.format(self.id)

    @requires_auth
    def delete(self):
        """Delete this card.

        :returns: bool
        """
        url = self._build_url(
            'projects/columns/cards', self.id, base_url=self._github_url)
        return self._boolean(self._delete(
            url, headers=Project.CUSTOM_HEADERS), 204, 404)

    @requires_auth
    def move(self, position, column_id):
        """Move this card.

        :param str position: (required), can be one of `top`, `bottom`, or
            `after:<card-id>`, where `<card-id>` is the id value of a card
            in the same column, or in the new column specified by `column_id`.
        :param int column_id: (required), the id value of a column in the
            same project.
        :returns: bool
        """
        if not position or not column_id:
            return False

        url = self._build_url(
            'projects/columns/cards',
            self.id,
            'moves',
            base_url=self._github_url
        )
        data = {'position': position, 'column_id': column_id}
        return self._boolean(self._post(
            url, data=data, headers=Project.CUSTOM_HEADERS), 201, 404)

    @requires_auth
    def update(self, note=None):
        """Update this card.

        :param str note: (optional), the card's note content. Only valid for
            cards without another type of content, so this cannot be specified
            if the card already has a content_id and content_type.
        :returns: bool
        """
        data = {'note': note}
        json = None
        self._remove_none(data)

        if data:
            url = self._build_url(
                'projects/columns/cards', self.id, base_url=self._github_url)
            json = self._json(self._patch(
                url, data=dumps(data), headers=Project.CUSTOM_HEADERS), 200)

        if json:
            self._update_attributes(json)
            return True
        return False
