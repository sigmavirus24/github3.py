import github3

from .helper import IntegrationHelper


class TestRepository(IntegrationHelper):
    def test_create_empty_blob(self):
        """Test the ability to create an empty blob on a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_empty_blob')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            blob_sha = repository.create_blob('', 'utf-8')

        assert blob_sha is not None
        assert blob_sha != ''

    def test_create_deployment(self):
        """Test the ability to create a deployment for a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_deployment')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = repository.create_deployment('0.8.2')

        assert isinstance(deployment, github3.repos.deployment.Deployment)

    def test_create_release(self):
        """Test the ability to create a release on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'charade')
            assert repository is not None
            release = repository.create_release(
                '1.0.3.test', 'f1d4e150be7070adfbbdca164328d69723e096ec',
                'Test release'
                )

        assert isinstance(release, github3.repos.release.Release)

    def test_iter_deployments(self):
        """Test that a repository's deployments may be retrieved."""
        cassette_name = self.cassette_name('iter_deployments')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for d in repository.iter_deployments():
                assert isinstance(d, github3.repos.deployment.Deployment)

    def test_iter_issues_accepts_state_all(self):
        """Test that the state parameter accets 'all'."""
        cassette_name = self.cassette_name('issues_state_all')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            for issue in repository.iter_issues(state='all'):
                assert issue.state in ('open', 'closed')

    def test_iter_languages(self):
        """Test that a repository's languages can be retrieved."""
        cassette_name = self.cassette_name('iter_languages')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for l in repository.iter_languages():
                assert 'ETag' not in l
                assert 'Last-Modified' not in l
                assert isinstance(l, tuple)

    def test_iter_pulls_accepts_sort_and_direction(self):
        """Test that iter_pulls now takes a sort parameter."""
        cassette_name = self.cassette_name('pull_requests_accept_sort')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            last_pr = None
            for pr in repository.iter_pulls(sort='updated', direction='asc'):
                assert pr
                if last_pr:
                    assert last_pr.updated_at < pr.updated_at
                last_pr = pr

    def test_iter_releases(self):
        """Test the ability to iterate over releases on a repository."""
        cassette_name = self.cassette_name('iter_releases')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for release in repository.iter_releases():
                assert isinstance(release, github3.repos.release.Release)

    def test_milestone(self):
        """
        Test the ability to retrieve a specific milestone on a repository.
        """
        cassette_name = self.cassette_name('milestone')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            milestone = repository.milestone(7)
        assert isinstance(milestone, github3.issues.milestone.Milestone)

    def test_release(self):
        """Test the ability to retrieve a single release."""
        cassette_name = self.cassette_name('release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            release = repository.release(76677)

        assert isinstance(release, github3.repos.release.Release)
