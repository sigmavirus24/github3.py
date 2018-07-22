import github3

from .helper import IntegrationHelper


class TestMilestone(IntegrationHelper):
    def test_delete(self):
        """Test the ability to delete a milestone."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            milestone = repository.create_milestone('test-milestone')
            assert milestone.delete() is True

    def test_update(self):
        """Test the ability to update a milestone."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            milestone = repository.create_milestone('test-milestone')
            assert milestone.update(
                title='integration', description='delete me'
            ) is True
            assert milestone.delete() is True

    def test_labels(self):
        """Test the ability to iterate over milestone labels."""
        cassette_name = self.cassette_name('labels')
        with self.recorder.use_cassette(cassette_name):
            issue = self.gh.issue('sigmavirus24', 'github3.py', 206)
            milestone = issue.milestone
            assert milestone is not None
            for label in milestone.labels():
                assert isinstance(label, github3.issues.label.ShortLabel)
