"""Integration tests for the User class."""
import github3

from .helper import IntegrationHelper


class TestUser(IntegrationHelper):

    """Integration tests for methods on the User class."""

    def test_events(self):
        """Show that a user can retrieve a events performed by a user."""
        cassette_name = self.cassette_name('events')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            events = list(user.events(25))

        assert len(events) > 0
        for event in events:
            assert isinstance(event, github3.events.Event)

    def test_organizations(self):
        """Show that a user can retrieve any user's organizations."""
        cassette_name = self.cassette_name('organizations')
        with self.recorder.use_cassette(cassette_name):
            u = self.gh.user('sigmavirus24')
            for o in u.organizations(number=25):
                assert isinstance(o, github3.orgs.Organization)
