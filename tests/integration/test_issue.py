"""Integration tests for Issues."""
import github3

from .helper import IntegrationHelper


class TestIssue(IntegrationHelper):

    """Integration tests for methods on the Issue class."""

    def test_comments(self):
        """Test the ability to retrieve comments on an issue."""
        cassette_name = self.cassette_name('comments')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 187)
            assert issue is not None
            comments = list(issue.comments())

        assert len(comments) > 0
        for comment in comments:
            assert isinstance(comment, github3.issues.comment.IssueComment)

    def test_events(self):
        """Test the ability to iterate over issue events."""
        self.token_login()
        cassette_name = self.cassette_name('events')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issue = repository.issue(218)
            for event in issue.events():
                assert isinstance(event, github3.issues.event.IssueEvent)
                assert event.issue is None
                assert isinstance(event.actor, github3.users.User)

    def test_labels(self):
        """Test the ability to iterate over issue labels."""
        cassette_name = self.cassette_name('labels')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 187)
            assert issue is not None
            for label in issue.labels():
                assert isinstance(label, github3.issues.label.Label)

    def test_pull_request(self):
        """Test the ability to retrieve the PR associated with an issue."""
        cassette_name = self.cassette_name('pull_request')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 301)
            assert issue is not None
            pull_request = issue.pull_request()

        assert isinstance(pull_request, github3.pulls.PullRequest)
