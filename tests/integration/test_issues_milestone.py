import github3

from .helper import IntegrationHelper


class TestMilestone(IntegrationHelper):
    def test_iter_labels(self):
        """Test the ability to iterate over milestone labels."""
        cassette_name = self.cassette_name('iter_labels')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 206)
            milestone = issue.milestone
            assert milestone is not None
            for label in milestone.iter_labels():
                assert isinstance(label, github3.issues.label.Label)
