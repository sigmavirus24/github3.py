# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Project."""

import github3

from .helper import IntegrationHelper


class TestProject(IntegrationHelper):
    """Project integration tests."""

    def test_column(self):
        """Test the ability to retrieve a single project column."""
        self.token_login()
        cassette_name = self.cassette_name('column')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400903)

            # Grab a project, any project
            first_column = next(project.columns())

            fetched_column = project.column(first_column.id)
            assert first_column == fetched_column

    def test_columns(self):
        """Test the ability to retrieve an project's columns."""
        self.token_login()
        cassette_name = self.cassette_name('columns')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400903)

            for column in project.columns():
                assert isinstance(column, github3.projects.ProjectColumn)

    def test_create_column(self):
        """Test the ability to create a column in a project."""
        self.token_login()
        cassette_name = self.cassette_name('create_column')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400903)
            column = project.create_column('test column')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert column.delete() is True

    def test_delete(self):
        """Test the ability to delete a Project."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400435)
            assert project.delete()

    def test_update(self):
        """Show that one can update a Project."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400435)
            assert project.update(project.name, project.body) is True


class TestProjectColumn(IntegrationHelper):
    """ProjectColumn integration tests."""

    def test_delete(self):
        """Test the ability to delete a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            column = repository.project(400903).column(698995)
            assert column.delete()

    def test_move(self):
        """Show that one can move a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('move')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400903)
            column = project.column(698995)
            column.move('first')
            assert list(project.columns())[0] == column

    def test_update(self):
        """Show that one can update a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            column = repository.project(400903).column(698994)
            assert column.update(column.name) is True
