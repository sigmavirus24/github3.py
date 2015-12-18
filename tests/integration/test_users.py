"""Integration tests for the User class."""
import github3
import datetime
import pytest

from .helper import IntegrationHelper
from github3.exceptions import MethodNotAllowed


class TestKey(IntegrationHelper):
    """Integration tests for methods on Key class."""

    def test_delete(self):
        """Test the ability to delete a key."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            key = self.gh.key(14947878)
            assert key.delete()

    def test_update(self):
        """Test the ability to update a key."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            key = self.gh.key(14948033)
            key_text = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD5T3fBQaqmCsJ'
                        'gHvDmlxpF89/nmb9V7sx30pTNPR9h1o/WEwJCdKIoqYcBRnoMUG'
                        'vGRBh/irJF+jOs4iLm5rd3nC44EIFfUyaHIzMaCbt8VuauEEQLV'
                        '/Rvgd8e0bYd4oaOrUhPhcSZPU9lMDopa8Gmf+6bt+HFIyDnUDPP'
                        'KT6jb0YohZgGs57db7Z+exlfrtuQ9Wk+n5Xa9OSQSOSlBzRlS6+'
                        'h/LLpTWUdFskxXjdFFZh5viGW2oUzLQ6eoNpx/sl2k/rpJGaqXe'
                        '4aoskG0v7pmymdipnQOep3eNeOUJSqiue17qzsvULU9Zk4ZUYZC'
                        '/8f7o4GtuLCKvIB+EdkVKbl mattchung@Matts-Air')
            with pytest.raises(MethodNotAllowed):
                key.update(title='Integration Test', key=key_text)


class TestUser(IntegrationHelper):

    """Integration tests for methods on the User class."""

    def test_email_addresses(self):
        """Test the ability to retrieve the email addresses of the
        authenticated user."""
        self.token_login()
        cassette_name = self.cassette_name('email_addresses')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.me()
            assert user is not None
            for address in user.email_addresses():
                assert isinstance(address, github3.users.UserEmail)

    def test_events(self):
        """Show that a user can retrieve a events performed by a user."""
        cassette_name = self.cassette_name('events')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            events = list(user.events(25))

        assert len(events) > 0
        for event in events:
            assert isinstance(event, github3.events.Event)

    def test_followers(self):
        """Show that a user can retrieve any user's followers."""
        cassette_name = self.cassette_name('followers')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            followers = list(user.followers(50))

        assert len(followers) > 0
        for follower in followers:
            assert isinstance(follower, github3.users.User)

    def test_following(self):
        """Show that a user can retrieve users that a user is following."""
        cassette_name = self.cassette_name('following')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            following = list(user.following(50))

        assert len(following) > 0
        for person in following:
            assert isinstance(person, github3.users.User)

    def test_keys(self):
        """Show that a user can retrieve any user's public keys."""
        cassette_name = self.cassette_name('keys')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            keys = list(user.keys())

        assert len(keys) > 0
        for key in keys:
            assert isinstance(key, github3.users.Key)

    def test_organization_events(self):
        """Show that a user can retrieve their events on an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('organization_events')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            events = list(user.organization_events('pdfkit', 25))

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

    def test_received_events(self):
        """Show that a user can retrieve any user's received events."""
        cassette_name = self.cassette_name('received_events')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            events = list(user.received_events(number=25))

        assert len(events) > 0
        for event in events:
            assert isinstance(event, github3.events.Event)

    def test_starred_repositories(self):
        """Show that a user can retrieve the repositories starred by a user."""
        cassette_name = self.cassette_name('starred_repositories')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            repos = list(user.starred_repositories(50))

        assert len(repos) > 0
        for starred in repos:
            assert isinstance(starred, github3.repos.Repository)
            assert isinstance(starred.starred_at, datetime.datetime)

    def test_subscriptions(self):
        """Show that a user can retrieve the repos subscribed to by a user."""
        cassette_name = self.cassette_name('subscriptions')
        with self.recorder.use_cassette(cassette_name):
            user = self.gh.user('sigmavirus24')
            repos = list(user.subscriptions())

        assert len(repos) > 0
        for repository in repos:
            assert isinstance(repository, github3.repos.Repository)
