"""Integration test for Notifications."""
import github3
from .helper import IntegrationHelper


class TestThread(IntegrationHelper):
    """Integration test for methods on Test class."""

    def test_subscription(self):
        """Show that a user can retrieve notifications for repository."""
        self.token_login()
        cassette_name = self.cassette_name("subscription")
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            threads = list(repository.notifications(all=True))
            assert len(threads) > 0
            thread = threads[0]
            assert isinstance(thread, github3.notifications.Thread)
            assert isinstance(thread.subscription(),
                              github3.notifications.ThreadSubscription)


class TestThreadSubscription(IntegrationHelper):
    """Integration test for methods on Test class."""

    def test_set(self):
        """Show that user can successful set subscription."""
        self.token_login()
        cassette_name = self.cassette_name("set")
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            threads = list(repository.notifications(all='true'))
            assert len(threads) > 0
            subscription = threads[0].subscription()
            assert subscription.set(True, False) is None
            assert isinstance(subscription,
                              github3.notifications.ThreadSubscription)
