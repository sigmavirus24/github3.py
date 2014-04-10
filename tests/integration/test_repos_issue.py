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
                assert isinstance(event.issue, github3.issues.Issue)
            assert event is not None
