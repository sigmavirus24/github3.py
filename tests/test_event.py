import base
from expecter import expect
from github3.event import Event
from github3.org import Organization


class TestEvent(base.BaseTest):
    def test_events(self):
        expect(Event.list_types()) != []

        events = self.g.list_events()
        expect(events) != []
        for e in events:
            self.assertIsNotNone(e.actor)
            self.assertIsNotNone(e.created_at)
            self.assertIsNotNone(e.id)
            if e.org:
                expect(e.org).isinstance(Organization)
            expect(e.payload).isinstance(dict)
            expect(e.is_public()).isinstance(bool)
            self.assertIsNotNone(e.repo)
            expect(e.repo).isinstance(tuple)
            self.assertIsNotNone(e.type)
