"""Deployment integration tests."""
import github3

from .helper import IntegrationHelper


def find(func, iterable):
    """Helper function to find the first item in an interable."""
    return next(iter(filter(func, iterable)))


class TestDeployment(IntegrationHelper):

    """Integration tests for the Deployment class."""

    def test_create_status(self):
        """Show that a user can create a deployment status."""
        self.token_login()
        cassette_name = self.cassette_name('create_status')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = find(lambda d: d.id == 801,
                              repository.deployments())
            assert deployment is not None
            status = deployment.create_status('success')

        assert isinstance(status, github3.repos.deployment.DeploymentStatus)

    def test_statuses(self):
        """Show that a user can retrieve deployment statuses."""
        cassette_name = self.cassette_name('statuses')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = find(lambda d: d.id == 801,
                              repository.deployments())
            assert deployment is not None
            statuses = list(deployment.statuses(5))

        for status in statuses:
            assert isinstance(status,
                              github3.repos.deployment.DeploymentStatus)
