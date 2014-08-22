"""Integration tests for the User class."""
import github3

from .helper import IntegrationHelper


class TestUser(IntegrationHelper):

    """Integration tests for methods on the User class."""

    def test_organizations(self):
        """Show that a user can retrieve any user's organizations."""
        cassette_name = self.cassette_name('organizations')
        with self.recorder.use_cassette(cassette_name):
            u = self.gh.user('sigmavirus24')
            for o in u.organizations(number=25):
                assert isinstance(o, github3.orgs.Organization)
