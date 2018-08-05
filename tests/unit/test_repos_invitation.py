"""Unit tests for Repository Invitation objects."""
import github3

from . import helper

get_invitation_example_data = helper.create_example_data_helper(
    'repos_invitation_example'
)
example_invitation_data = get_invitation_example_data()

url_for_invitee = helper.create_url_helper(example_invitation_data['url'])
url_for_inviter = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/invitations/1'
)


class TestInvitation(helper.UnitHelper):
    """Unit tests for the Invitation object."""

    described_class = github3.repos.invitation.Invitation
    example_data = example_invitation_data

    def test_accept(self):
        """Verify the request to accept an invitation."""
        self.instance.accept()

        self.session.patch.assert_called_once_with(
            url_for_invitee()
        )

    def test_decline(self):
        """Verify the request to decline an invitation."""
        self.instance.decline()

        self.session.delete.assert_called_once_with(
            url_for_invitee()
        )

    def test_delete(self):
        """Verify the request to delete an invitation."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            url_for_inviter()
        )

    def test_update(self):
        """Verify the request to update an invitation."""
        self.instance.update(permissions='admin')

        self.session.patch.assert_called_once_with(
            url_for_inviter(),
            data='{"permissions": "admin"}'
        )


class TestInvitationRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    """Unit tests that demonstrate which Invitation methods require auth."""

    described_class = github3.repos.invitation.Invitation
    example_data = example_invitation_data

    def test_accept(self):
        """Show that you must be authenticated to accept an invitation."""
        self.assert_requires_auth(self.instance.accept)

    def test_decline(self):
        """Show that you must be authenticated to decline an invitation."""
        self.assert_requires_auth(self.instance.decline)

    def test_delete(self):
        """Show that you must be authenticated to delete an invitation."""
        self.assert_requires_auth(self.instance.delete)

    def test_update(self):
        """Show that you must be authenticated to update an invitation."""
        self.assert_requires_auth(self.instance.update)
