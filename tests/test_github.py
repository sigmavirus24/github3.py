import base
import github3

class TestGitHub(base.BaseTest):
    def setUp(self):
        super(TestGitHub, self).setUp()
        self.fake_auth = ('fake_user', 'fake_password')
        self.fake_oauth = 'foobarbogusoauth'

    def test_login(self):
        g = github3.GitHub()
        # Test "regular" auth
        g.login(*self.fake_auth)
        self.failUnlessEqual(self.fake_auth, g._session.auth)
        # Test "oauth" auth
        g.login(token=self.fake_oauth)
        self.failUnlessEqual(g._session.headers['Authorization'],
                'token ' + self.fake_oauth)
        try:
            g.user()
        except github3.Error:
            pass
        except Exception:
            self.fail("Uncaught exception")

    #def test_create_gist(self):
    #    pass
