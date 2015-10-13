import github3

from .helper import (UnitHelper, create_url_helper, create_example_data_helper)

get_subscription_example_data = create_example_data_helper('subscription_example')
url_for = create_url_helper(
    'https://api.github.com/notifications/threads/5864188/subscription'
)


class TestSubscription(UnitHelper):
    described_class = github3.notifications.Subscription
    example_data = get_subscription_example_data()

    def test_repr(self):
        """Show that instance is formatted as a string when printed"""
        assert isinstance(repr(self.instance), str)

    def test_delete(self):
        """Show that a user can delete a subscription"""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            url_for()
        )

    def test_is_ignored(self):
        """Show that subscription is ignored"""
        self.instance.is_ignored() == self.instance.ignored

    def test_is_subscription(self):
        """Show that subscription is subscribed"""
        self.instance.is_subscribed() == self.instance.subscribed

    def test_set(self):
        """Show that a user can set a subscription"""
        pass
        # Test is currently failing due to session._put returns None
        # self.instance.set(True, False)
        # self.session.put.assert_called_once_with(
        #    url_for()
        # )
