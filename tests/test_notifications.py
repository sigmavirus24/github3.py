import github3
import datetime
from tests.utils import BaseCase, load


class TestThread(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestThread, self).__init__(methodName)
        self.thread = github3.notifications.Thread(load('notification'))
        self.api = ("https://api.github.com/notifications/threads/6169361")

    def test_equality(self):
        t = github3.notifications.Thread(load('notification'))
        assert self.thread == t
        t._uniq = 1
        assert self.thread != t

    def test_last_read_at(self):
        json = self.thread.to_json().copy()
        json['last_read_at'] = '2013-12-31T23:59:59Z'
        t = github3.notifications.Thread(json)
        assert isinstance(t.last_read_at, datetime.datetime)

    def test_repr(self):
        assert repr(self.thread) == '<Thread [{0}]>'.format(
            self.thread.subject.get('title'))

    def test_delete_subscription(self):
        self.response('', 204)
        self.delete(self.api + '/subscription')

        assert self.thread.delete_subscription()
        self.mock_assertions()

    def test_is_unread(self):
        assert self.thread.is_unread() == self.thread.unread

    def test_mark(self):
        self.response('', 205)
        self.patch(self.api)
        self.conf = {}

        assert self.thread.mark()
        self.mock_assertions()

    def test_set_subscription(self):
        self.response('subscription')
        self.put(self.api + '/subscription')
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        assert isinstance(self.thread.set_subscription(True, False),
                          github3.notifications.Subscription)
        self.mock_assertions()

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

    def test_repr(self):
        assert isinstance(repr(self.subscription), str)

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        assert self.subscription.delete()
        self.mock_assertions()

    def test_is_ignored(self):
        assert self.subscription.is_ignored() == self.subscription.ignored

    def test_is_subscription(self):
        subbed = self.subscription.is_subscribed()
        assert subbed == self.subscription.subscribed

    def test_set(self):
        self.response('subscription')
        self.put(self.api)
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        assert self.subscription.set(True, False) is None
        self.mock_assertions()
