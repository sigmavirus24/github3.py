from base import BaseTest, expect, str_test
from github3.events import Event, _payload_handlers
from github3.orgs import Organization
from github3.repos import RepoComment, Download


class TestEvent(BaseTest):
    def __test_events(self, events):
        expect(events) != []
        for e in events:
            self.assertAreNotNone(e, 'actor', 'created_at', 'id', 'repo',
                    'type')
            if e.org:
                expect(e.org).isinstance(Organization)

            payload = (dict, str_test[0], str_test[1])
            expect(e.payload).isinstance(payload)
            expect(e.is_public()).isinstance(bool)
            expect(e.to_json()).isinstance(dict)
            expect(e.repo).isinstance(tuple)
            expect(repr(e)).is_not_None()

    def test_events(self):
        expect(Event.list_types()) != []

        events = self.g.list_events()
        self.__test_events(events)

        if self.auth:
            user = self._g.user()
            for public in (True, False):
                events = user.list_events(public)
                self.__test_events(events)


def handler(name):
    return _payload_handlers[name]


class TestPayloadHandlers(BaseTest):
    def test_commitcomment(self):
        h = handler('CommitCommentEvent')
        p = h({
            'comment': {
                'html_url': '',
                'commit_id': '',
                'line': '',
                'path': '',
                'pos': '',
                'updated_at': '',
                'user': {}
                }
            })
        expect(p['comment']).isinstance(RepoComment)

    def test_download(self):
        h = handler('DownloadEvent')
        p = h({
            'download': {
                'url': '',
                'html_url': '',
                'id': '',
                'name': '',
                'description': '',
                'size': '',
                'download_count': 0,
                'content_type': ''
                }
            })
        expect(p['download']).isinstance(Download)
