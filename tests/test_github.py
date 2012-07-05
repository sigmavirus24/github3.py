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
        h = github3.login(*self.fake_auth)
        for i in [g, h]:
            self.failUnlessEqual(self.fake_auth, i._session.auth)
        # Test "oauth" auth
        g.login(token=self.fake_oauth)
        h = github3.login('', '', token=self.fake_oauth)
        for i in [g, h]:
            self.failUnlessEqual(i._session.headers['Authorization'],
                    'token ' + self.fake_oauth)

        self.assertRaisesError(g.user)

    def test_gist(self):
        # My gcd example
        gist_id = 2648112
        g = github3.GitHub()
        if not g.gist(gist_id):
            self.fail('Check gcd gist')

        self.assertRaisesError(g.gist, -1)

    def test_following(self):
        g = github3.GitHub()
        self.assertRaisesError(g.is_following, 'sigmavirus24')
        self.assertRaisesError(g.follow, 'sigmavirus24')
        self.assertRaisesError(g.unfollow, 'sigmavirus24')
        self.assertRaisesError(g.list_followers)
        self.assertIsNotNone(g.list_followers('kennethreitz'))
        self.assertRaisesError(g.list_following)
        self.assertIsNotNone(g.list_following('kennethreitz'))

    def test_watching(self):
        g = github3.GitHub()
        sigm, todo = self.sigm, self.todo
        self.assertRaisesError(g.watch, sigm, todo)
        self.assertRaisesError(g.unwatch, sigm, todo)
        self.assertRaisesError(g.list_watching)
        self.assertIsNotNone(g.list_watching(sigm))
        self.assertRaisesError(g.is_watching, sigm, todo)
        self.assertRaisesError(g.watch, sigm, todo)
        self.assertRaisesError(g.unwatch, sigm, todo)

    def test_create_gist(self):
        pass

    def test_create_issue(self):
        g = github3.GitHub()
        sigm, todo = self.sigm, self.todo
        title = 'Test issue for github3.py'
        self.assertRaisesError(g.create_issue, sigm, todo, title)
    
    def test_create_key(self):
        g = github3.GitHub()
        self.assertRaisesError(g.create_key, 'Foo bar', 'bogus')

    def test_create_repo(self):
        g = github3.GitHub()
        self.assertRaisesError(g.create_repo, 'test_github3.py')
