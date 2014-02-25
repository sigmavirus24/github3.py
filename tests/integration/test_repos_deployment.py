import github3

from .helper import IntegrationHelper


def find(func, iterable):
    return next(iter(filter(func, iterable)))


class TestDeployment(IntegrationHelper):
    def test_create_status(self):
        """
        Test that using a Deployment instance, a user can create a status.
        """
        self.basic_login()
        cassette_name = self.cassette_name('create_status')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = find(lambda d: d.id == 801,
                              repository.iter_deployments())
            assert deployment is not None
            status = deployment.create_status('success')

        assert isinstance(status, github3.repos.deployment.DeploymentStatus)

    def test_iter_statuses(self):
        """
        Test that using a Deployment instance, a user can retrieve statuses.
        """
        cassette_name = self.cassette_name('statuses')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = find(lambda d: d.id == 801,
                              repository.iter_deployments())
            assert deployment is not None
            statuses = list(deployment.iter_statuses(5))

        for status in statuses:
            assert isinstance(status,
                              github3.repos.deployment.DeploymentStatus)
