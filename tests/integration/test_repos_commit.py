"""Integration tests for Repository Commit objects."""
import github3

from . import helper


class TestRepoCommit(helper.IntegrationHelper):
    """Integration tests for the RepoCommit object."""

    def test_status(self):
        """Verify that we can retrieve the combined status for a commit."""
        cassette_name = self.cassette_name('status')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.commit(
                '9aa43ea48c762b19e8191ae2c5c5fcb87fe30b44'
            )
            combined_status = commit.status()
        assert isinstance(combined_status, github3.repos.status.CombinedStatus)

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

    def test_comments(self):
        """Test the ability to retrieve comments on a commit."""
        cassette_name = self.cassette_name('comments')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('octocat', 'Hello-World')
            commit = repository.commit(
                '553c2077f0edc3d5dc5d17262f6aa498e69d6f8e'
            )
            comments = list(commit.comments())

        for comment in comments:
            assert isinstance(comment, github3.repos.comment.RepoComment)

    def test_author_is_not_committer(self):
        """Test we are not confusing author and committer on a commit."""
        cassette_name = self.cassette_name('author_committer')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.commit(
                '6a0470c992dd97d97fa0fee503153b125141ca4c'
            )
            assert commit.author != commit.committer
