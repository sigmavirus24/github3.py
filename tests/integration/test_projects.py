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
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)

            # Grab a project, any project
            first_column = next(project.columns())

            fetched_column = project.column(first_column.id)
            assert first_column == fetched_column

    def test_columns(self):
        """Test the ability to retrieve an project's columns."""
        self.token_login()
        cassette_name = self.cassette_name('columns')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)

            for column in project.columns():
                assert isinstance(column, github3.projects.ProjectColumn)

    def test_create_column(self):
        """Test the ability to create a column in a project."""
        self.token_login()
        cassette_name = self.cassette_name('create_column')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert column.delete() is True

    def test_delete(self):
        """Test the ability to delete a Project."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.create_project('delete-me')
            assert project.delete()

    def test_update(self):
        """Show that one can update a Project."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            assert project.update(project.name, project.body) is True


class TestProjectColumn(IntegrationHelper):
    """ProjectColumn integration tests."""

    def test_card(self):
        """Test the ability to retrieve a single project card."""
        self.token_login()
        cassette_name = self.cassette_name('card')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            card = column.create_card_with_note('Delete mmeeeeeeee')

            fetched_card = column.card(card.id)
            assert card == fetched_card
            card.delete()
            column.delete()

    def test_cards(self):
        """Test the ability to retrieve an project's cards."""
        self.token_login()
        cassette_name = self.cassette_name('cards')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            card = column.create_card_with_note('Delete mmeeeeeeee')
            assert card is not None

            for card in column.cards():
                assert isinstance(card, github3.projects.ProjectCard)

            card.delete()
            column.delete()

    def test_create_card_with_content_id(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_content_id')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            issues = list(repository.issues())
            card = column.create_card_with_content_id(issues[0].id, 'Issue')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True
            column.delete()

    def test_create_card_with_issue(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_issue')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            issues = list(repository.issues())
            card = column.create_card_with_issue(issues[0])
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True
            column.delete()

    def test_create_card_with_note(self):
        """Test the ability to create a note card in project column."""
        self.token_login()
        cassette_name = self.cassette_name('create_card_with_note')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            card = column.create_card_with_note('note content')
            assert isinstance(column, github3.projects.ProjectColumn)
            assert card.delete() is True
            column.delete()

    def test_delete(self):
        """Test the ability to delete a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            assert column.delete()

    def test_move(self):
        """Show that one can move a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('move')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            column.move('first')
            assert list(project.columns())[0] == column
            column.delete()

    def test_update(self):
        """Show that one can update a ProjectColumn."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            assert column.update('test column rename') is True
            column.delete()


class TestProjectCard(IntegrationHelper):
    """ProjectCard integration tests."""

    def test_delete(self):
        """Test the ability to delete a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            card = column.create_card_with_note('note content')
            assert card.delete()
            column.delete()

    def test_move(self):
        """Show that one can move a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('move')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            topcard = column.create_card_with_note('note content')
            bottomcard = column.create_card_with_note('bottom note')
            bottomcard.move('top', column.id)
            assert list(column.cards())[0] == bottomcard
            topcard.delete()
            bottomcard.delete()
            column.delete()

    def test_update(self):
        """Show that one can update a ProjectCard."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.project(1177360)
            column = project.create_column('test column')
            card = column.create_card_with_note('note content')
            assert card.update('new note content') is True
            card.delete()
            column.delete()
