import github3
from tests.utils import BaseCase, load


class TestThread(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestThread, self).__init__(methodName)
        self.thread = github3.notifications.Thread(load('notification'))
        self.api = ("https://api.github.com/notifications/threads/6169361")

    def test_subscription(self):
        self.response('subscription')
        self.get(self.api + '/subscription')

        assert isinstance(self.thread.subscription(),
                          github3.notifications.Subscription)
        self.mock_assertions()


class TestSubscription(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestSubscription, self).__init__(methodName)
        self.subscription = github3.notifications.Subscription(
            load('subscription'))
        self.api = ("https://api.github.com/notifications/threads/5864188/"
                    "subscription")

    def test_set(self):
        self.response('subscription')
        self.put(self.api)
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        assert self.subscription.set(True, False) is None
        self.mock_assertions()
