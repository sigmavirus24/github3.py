import base
from github3 import GitHub

class TestGitHub(base.BaseTest):
    def setUp(self):
        super(TestGitHub, self).setUp()
        self.fake_auth = ('fake_user', 'fake_password')
        self.fake_oauth = 'foobarbogusoauth'

    def test_login(self):
        g = GitHub()
        g.login(**self.fake_auth)
        self.failUnlessEqual(self.fake_auth, g._session.auth)
        g.login(oauth=self.fake_oauth)
        self.failUnlessEqual(g._session.headers['Authorization'],
                'token ' + self.fake_oauth)
