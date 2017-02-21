# -*- coding: utf-8 -*-
"""Unit tests for the github3.projects module."""
import pytest

from . import helper

from github3 import GitHubError
from github3 import projects


get_project_example_data = helper.create_example_data_helper(
    'project_example'
)

url_for = helper.create_url_helper(
    'https://api.github.com/projects/1002604'
)


class TestProject(helper.UnitHelper):
    """Project unit tests."""

    described_class = projects.Project
    example_data = get_project_example_data()

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

    def test_delete(self):
        """Verify that deleting a project requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete()

    def test_update(self):
        """Verfiy that updating a project requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.update('name', 'body')
