import github3

from .helper import IntegrationHelper


class TestIssue(IntegrationHelper):
    def test_iter_events(self):
        """Test the ability to iterate over issue events."""
        self.token_login()
        cassette_name = self.cassette_name('iter_events')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issue = repository.issue(218)
            for event in issue.iter_events():
                assert isinstance(event, github3.issues.event.IssueEvent)
                assert event.issue is None
                assert isinstance(event.actor, github3.users.User)

    def test_iter_labels(self):
        """Test the ability to iterate over issue labels."""
        cassette_name = self.cassette_name('iter_labels')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 187)
            assert issue is not None
            for label in issue.iter_labels():
                assert isinstance(label, github3.issues.label.Label)
