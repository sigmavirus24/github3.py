# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Project."""

from .helper import IntegrationHelper


class TestProject(IntegrationHelper):
    """Project integration tests."""

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
