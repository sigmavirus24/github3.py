import base

class TestEvent(base.BaseTest):
    def test_events(self):
        events = self.g.list_events()
        assert events != []
