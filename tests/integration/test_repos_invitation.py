"""Integration tests for Repository Invitation objects."""
import github3

from . import helper


class TestInvitation(helper.IntegrationHelper):
    """Integration tests for the Invitation object."""

    def test_accept(self):
        """Test the ability to accept an invitation."""
        self.token_login()
        cassette_name = self.cassette_name('accept')
        with self.recorder.use_cassette(cassette_name):
            for invitation in self.gh.repository_invitations():
                assert invitation.accept() is True

    def test_decline(self):
        """Test the ability to decline an invitation."""
        self.token_login()
        cassette_name = self.cassette_name('decline')
        with self.recorder.use_cassette(cassette_name):
            for invitation in self.gh.repository_invitations():
                assert invitation.decline() is True

    def test_delete(self):
        """Test the ability to delete an invitation."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            for invitation in repository.invitations():
                assert invitation.delete() is True

    def test_update(self):
        """Test the ability to update an invitation."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            for invitation in repository.invitations():
                updated_invitation = invitation.update(permissions='admin')
                assert isinstance(
                    updated_invitation, github3.repos.invitation.Invitation)
