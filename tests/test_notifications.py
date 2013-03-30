import github3
import datetime
from tests.utils import BaseCase, load, expect


class TestThread(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestThread, self).__init__(methodName)
        self.thread = github3.notifications.Thread(load('notification'))
        self.api = ("https://api.github.com/notifications/threads/6169361")

    def test_equality(self):
        t = github3.notifications.Thread(load('notification'))
        expect(self.thread) == t
        t.id = 1
        expect(self.thread) != t

    def test_last_read_at(self):
        json = self.thread.to_json().copy()
        json['last_read_at'] = '2013-12-31T23:59:59Z'
        t = github3.notifications.Thread(json)
        expect(t.last_read_at).isinstance(datetime.datetime)

    def test_repr(self):
        expect(repr(self.thread)) == '<Thread [{0}]>'.format(
            self.thread.subject.get('title'))

    def test_delete_subscription(self):
        self.response('', 204)
        self.delete(self.api + '/subscription')

        expect(self.thread.delete_subscription()).is_True()
        self.mock_assertions()

    def test_is_unread(self):
        expect(self.thread.is_unread()) == self.thread.unread

    def test_mark(self):
        self.response('', 205)
        self.patch(self.api)
        self.conf = {}

        expect(self.thread.mark()).is_True()
        self.mock_assertions()

    def test_set_subscription(self):
        self.response('subscription')
        self.put(self.api + '/subscription')
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        expect(self.thread.set_subscription(True, False)).isinstance(
            github3.notifications.Subscription)
        self.mock_assertions()

    def test_subscription(self):
        self.response('subscription')
        self.get(self.api + '/subscription')

        expect(self.thread.subscription()).isinstance(
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
        expect(repr(self.subscription)) == '<Subscription [True]>'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        expect(self.subscription.delete()).is_True()
        self.mock_assertions()

    def test_is_ignored(self):
        expect(self.subscription.is_ignored()) == self.subscription.ignored

    def test_is_subscription(self):
        subbed = self.subscription.is_subscribed()
        expect(subbed) == self.subscription.subscribed

    def test_set(self):
        self.response('subscription')
        self.put(self.api)
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        expect(self.subscription.set(True, False)).is_None()
        self.mock_assertions()
