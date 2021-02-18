"""Unit tests around github4's Subscription classes."""
import github4
from .helper import create_example_data_helper
from .helper import create_url_helper
from .helper import UnitHelper

get_example_data = create_example_data_helper("subscription_example")
url_for = create_url_helper(
    "https://api.github.com/notifications/threads/1/subscription"
)


class TestSubscription(UnitHelper):
    """Subscription unit tests."""

    described_class = github4.notifications._Subscription
    example_data = get_example_data()

    def test_repr(self):
        """Show that instance is formatted as a string when printed."""
        assert isinstance(repr(self.instance), str)

    def test_delete(self):
        """Show that a user can delete a subscription."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(url_for())

    def test_set(self):
        """Show that a user can set a subscription."""
        self.instance._update_attributes = lambda *args: None
        self.instance.set(True, False)

        self.put_called_with(url_for(), data={"ignored": False, "subscribed": True})
