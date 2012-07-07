import base
from expecter import expect

class TestEvent(base.BaseTest):
    def test_events(self):
        events = self.g.list_events()
        expect(events) != []
