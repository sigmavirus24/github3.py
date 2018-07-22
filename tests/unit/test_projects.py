# -*- coding: utf-8 -*-
"""Unit tests for the github3.projects module."""
import pytest

from . import helper

from github3 import GitHubError
from github3 import issues
from github3 import projects


get_project_example_data = helper.create_example_data_helper(
    'project_example'
)
get_project_card_example_data = helper.create_example_data_helper(
    'project_card_example'
)
get_project_column_example_data = helper.create_example_data_helper(
    'project_column_example'
)
get_issue_example_data = helper.create_example_data_helper(
    'issue_example'
)


url_for = helper.create_url_helper(
    'https://api.github.com/projects/1002604'
)
card_url_for = helper.create_url_helper(
    'https://api.github.com/projects/columns/cards'
)
columns_url_for = helper.create_url_helper(
    'https://api.github.com/projects/columns'
)


class TestProject(helper.UnitHelper):
    """Project unit tests."""

    described_class = projects.Project
    example_data = get_project_example_data()

    def test_column(self):
        """Show that a user can get an existing project column by ID."""
        self.instance.column(367)
        self.session.get.assert_called_once_with(
            columns_url_for('367'),
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_create_column(self):
        """Show that a user can create a new project column."""
        self.instance.create_column('test column')
        self.post_called_with(
            url_for('columns'),
            data={'name': 'test column'},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_delete(self):
        """Show that a user can delete a Project."""
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            url_for(), headers=projects.Project.CUSTOM_HEADERS)

    def test_update(self):
        """Show that a user can update a Project."""
        self.instance.update('my new title', 'my new body')

        self.patch_called_with(
            url_for(),
            data={
                'name': 'my new title',
                'body': 'my new body'
            },
            headers=projects.Project.CUSTOM_HEADERS
        )


class TestProjectAuth(helper.UnitRequiresAuthenticationHelper):
    """Test Project methods that require authentication."""

    described_class = projects.Project
    example_data = get_project_example_data()

    def test_create_column(self):
        """Verify that creating a column requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_column('name')

    def test_delete(self):
        """Verify that deleting a project requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete()

    def test_update(self):
        """Verfiy that updating a project requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.update('name', 'body')


class TestProjectIterator(helper.UnitIteratorHelper):
    """Test Project methods that return iterators."""

    described_class = projects.Project
    example_data = get_project_example_data()

    def test_columns(self):
        """Show that a user can get a list of all columns in a project."""
        i = self.instance.columns()
        self.get_next(i)
        self.session.get.assert_called_once_with(
            url_for('columns'),
            params={'per_page': 100},
            headers=projects.Project.CUSTOM_HEADERS
        )


class TestProjectColumn(helper.UnitHelper):
    """ProjectColumn unit tests."""

    described_class = projects.ProjectColumn
    example_data = get_project_column_example_data()

    def test_card(self):
        """Show that a user can get an existing project card by ID."""
        self.instance.card(1478)
        self.session.get.assert_called_once_with(
            card_url_for('1478'),
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_create_card_with_content_id(self):
        """Show that a user can create a new project card with a content ID."""
        self.instance.create_card_with_content_id(1, 'Issue')
        self.post_called_with(
            columns_url_for('367/cards'),
            data={'content_id': 1, 'content_type': 'Issue'},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_create_card_with_issue(self):
        """Show that a user can create a new project card with an Issue."""
        issue_data = get_issue_example_data()
        issue = issues.Issue(issue_data, self.session)

        self.instance.create_card_with_issue(issue)
        self.post_called_with(
            columns_url_for('367/cards'),
            data={'content_id': 1, 'content_type': 'Issue'},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_create_card_with_note(self):
        """Show that a user can create a new project card with a note."""
        self.instance.create_card_with_note('a note')
        self.post_called_with(
            columns_url_for('367/cards'),
            data={'note': 'a note'},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_delete(self):
        """Show that a user can delete a ProjectColumn."""
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            columns_url_for('367'),
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_move(self):
        """Show that a user can move a ProjectColumn."""
        self.instance.move('after:3')
        self.post_called_with(
            columns_url_for('367/moves'),
            data={'position': 'after:3'},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_update(self):
        """Show that a user can update a ProjectColumn."""
        self.instance.update('my new title')

        self.patch_called_with(
            columns_url_for('367'),
            data={
                'name': 'my new title',
            },
            headers=projects.Project.CUSTOM_HEADERS
        )


class TestProjectColumnAuth(helper.UnitRequiresAuthenticationHelper):
    """Test ProjectColumn methods that require authentication."""

    described_class = projects.ProjectColumn
    example_data = get_project_column_example_data()

    def test_create_card_with_content_id(self):
        """Verify that creating a content ID card requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_card_with_content_id(1, 'Issue')

    def test_create_card_with_issue(self):
        """Verify that creating an issue card requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_card_with_issue(None)

    def test_create_card_with_note(self):
        """Verify that creating a card with a note requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_card_with_note('note')

    def test_delete(self):
        """Verify that deleting a column requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete()

    def test_update(self):
        """Verfiy that updating a column requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.update('name')


class TestProjectColumnIterator(helper.UnitIteratorHelper):
    """Test Project methods that return iterators."""

    described_class = projects.ProjectColumn
    example_data = get_project_column_example_data()

    def test_cards(self):
        """Show that a user can get a list of all cards in a project column."""
        i = self.instance.cards()
        self.get_next(i)
        self.session.get.assert_called_once_with(
            columns_url_for('367/cards'),
            params={'per_page': 100},
            headers=projects.Project.CUSTOM_HEADERS
        )


class TestProjectCard(helper.UnitHelper):
    """ProjectCard unit tests."""

    described_class = projects.ProjectCard
    example_data = get_project_card_example_data()

    def test_delete(self):
        """Show that a user can delete a ProjectCard."""
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            card_url_for('1478'),
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_move(self):
        """Show that a user can move a ProjectCard."""
        self.instance.move('after:3', 367)
        self.post_called_with(
            card_url_for('1478/moves'),
            data={'position': 'after:3', 'column_id': 367},
            headers=projects.Project.CUSTOM_HEADERS
        )

    def test_update(self):
        """Show that a user can update a ProjectCard."""
        self.instance.update('my new note')

        self.patch_called_with(
            card_url_for('1478'),
            data={
                'note': 'my new note',
            },
            headers=projects.Project.CUSTOM_HEADERS
        )


class TestProjectCardAuth(helper.UnitRequiresAuthenticationHelper):
    """Test ProjectCard methods that require authentication."""

    described_class = projects.ProjectCard
    example_data = get_project_card_example_data()

    def test_delete(self):
        """Verify that deleting a card requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete()

    def test_update(self):
        """Verfiy that updating a card requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.update('note')
