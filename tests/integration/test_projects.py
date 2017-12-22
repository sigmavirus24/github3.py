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

    def test_card(self):
        """Test the ability to retrieve a single project card."""
        self.token_login()
        cassette_name = self.cassette_name('card')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            column = repository.project(400903).column(698994)

            # Grab a column, any column
            first_card = next(column.cards())

            fetched_card = column.card(first_card.id)
            assert first_card == fetched_card

    def test_cards(self):
        """Test the ability to retrieve an project's cards."""
        self.token_login()
        cassette_name = self.cassette_name('cards')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            column = repository.project(400903).column(698994)

            for card in column.cards():
                assert isinstance(card, github3.projects.ProjectCard)

    def test_create_card_with_content_id(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_content_id')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issues = list(repository.issues())
            column = repository.project(400903).column(698994)
            card = column.create_card_with_content_id(issues[0].id, 'Issue')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True

    def test_create_card_with_issue(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_issue')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issues = list(repository.issues())
            column = repository.project(400903).column(698994)
            card = column.create_card_with_issue(issues[0])
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True

    def test_create_card_with_note(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_note')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            column = repository.project(400903).column(698994)
            card = column.create_card_with_note('note content')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True

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


class TestProjectCard(IntegrationHelper):
    """ProjectCard integration tests."""

    def test_delete(self):
        """Test the ability to delete a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            card = repository.project(400903).column(698994).card(1809795)
            assert card.delete()

    def test_move(self):
        """Show that one can move a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('move')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            project = repository.project(400903)
            column = project.column(698994)
            card = column.card(1809807)
            card.move('top', 698994)
            assert list(column.cards())[0] == card

    def test_update(self):
        """Show that one can update a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            card = repository.project(400903).column(698994).card(1809795)
            assert card.update(card.note) is True
