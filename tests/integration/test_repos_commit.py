"""Integration tests for Repository Commit objects."""
import github3

from . import helper


class TestRepoCommit(helper.IntegrationHelper):

    """Integration tests for the RepoCommit object."""

    def test_statuses(self):
        """Test the ability to retrieve statuses on a commit."""
        cassette_name = self.cassette_name('statuses')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.commit(
                '29eaea046b353723f80a4810e3f2ea9d16ea6c25'
            )
            statuses = list(commit.statuses())

        for status in statuses:
            assert isinstance(status, github3.repos.status.Status)
