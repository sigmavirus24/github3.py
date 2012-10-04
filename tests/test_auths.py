from .base import expect, expect_str, BaseTest
from datetime import datetime
from github3.auths import Authorization


class TestAuthorization(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestAuthorization, self).__init__(methodName)
        if not self.auth:
            json = {'scopes': ['public_repo'],
                    'url': 'https://api.github.com',
                    'app': {'url': 'travis-ci.org', 'name': 'Travis'},
                    'updated_at': '2012-09-28T03:43:11Z',
                    'id': 0,
                    'note': None,
                    'note_url': None,
                    'token': 'upupdowndownleftrightba',
                    'created_at': '2012-02-28T01:45:49Z',
                    }
            self.authorization = Authorization(json, None)
        else:
            self.authorization = self.g.authorize(self.user, self.pw, [])
        self.deleted = False

    def test_authorization(self):
        expect(self.authorization).isinstance(Authorization)
        expect(repr(self.authorization)) != ''

    def test_app(self):
        expect(self.authorization.app).isinstance(dict)

    def test_name(self):
        expect(self.authorization.name) == self.authorization.app.get('name',
                '')

    def test_token(self):
        expect(self.authorization.token) != ''

    def test_updated_at(self):
        expect(self.authorization.updated_at).isinstance(datetime)

    def test_created_at(self):
        expect(self.authorization.created_at).isinstance(datetime)

    def test_note(self):
        expect_str(self.authorization.note)

    def test_note_url(self):
        expect_str(self.authorization.note_url)

    def test_scopes(self):
        expect(self.authorization.scopes).isinstance(list)

    def test_update(self):
        if not self.auth:
            return

        if self.deleted:
            self.authorization = self._g.authorize(None, None, [])

        self.authorization.update(['repo', 'repo:status'], ['user'],
                ['repo:status'], 'https://github.com/sigmavirus24/github3.py')

        if self.deleted:
            self.authorization.delete()

    def test_delete(self):
        if not self.auth:
            return

        self.authorization.delete()
        self.deleted = True
