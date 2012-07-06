import base
import github3

class TestGitHub(base.BaseTest):
    def setUp(self):
        super(TestGitHub, self).setUp()
        self.fake_auth = ('fake_user', 'fake_password')
        self.fake_oauth = 'foobarbogusoauth'

    def test_login(self):
        # Test "regular" auth
        self.g.login(*self.fake_auth)
        h = github3.login(*self.fake_auth)
        for i in [self.g, h]:
            self.failUnlessEqual(self.fake_auth, i._session.auth)
        # Test "oauth" auth
        self.g.login(token=self.fake_oauth)
        h = github3.login('', '', token=self.fake_oauth)
        for i in [self.g, h]:
            self.failUnlessEqual(i._session.headers['Authorization'],
                    'token ' + self.fake_oauth)
        self.assertRaisesError(self.g.user)

    def test_gist(self):
        # My gcd example
        gist_id = 2648112
        if not self.g.gist(gist_id):
            self.fail('Check gcd gist')

        self.assertRaisesError(self.g.gist, -1)

    def test_following(self):
        self.assertRaisesError(self.g.is_following, 'sigmavirus24')
        self.assertRaisesError(self.g.follow, 'sigmavirus24')
        self.assertRaisesError(self.g.unfollow, 'sigmavirus24')
        self.assertRaisesError(self.g.list_followers)
        self.assertIsNotNone(self.g.list_followers('kennethreitz'))
        self.assertRaisesError(self.g.list_following)
        self.assertIsNotNone(self.g.list_following('kennethreitz'))

    def test_watching(self):
        sigm, todo = self.sigm, self.todo
        self.assertRaisesError(self.g.watch, sigm, todo)
        self.assertRaisesError(self.g.unwatch, sigm, todo)
        self.assertRaisesError(self.g.list_watching)
        self.assertIsNotNone(self.g.list_watching(sigm))
        self.assertRaisesError(self.g.is_watching, sigm, todo)
        self.assertRaisesError(self.g.watch, sigm, todo)
        self.assertRaisesError(self.g.unwatch, sigm, todo)

    def test_create_gist(self):
        pass

    def test_create_issue(self):
        sigm, todo = self.sigm, self.todo
        title = 'Test issue for github3.py'
        self.assertRaisesError(self.g.create_issue, sigm, todo, title)
    
    def test_create_key(self):
        self.assertRaisesError(self.g.create_key, 'Foo bar', 'bogus')

    def test_create_repo(self):
        self.assertRaisesError(self.g.create_repo, 'test_github3.py')

    def test_delete_key(self):
        self.assertRaisesError(self.g.delete_key, -1)

    def test_get_key(self):
        self.assertRaisesError(self.g.get_key, -1)

    def test_issue(self):
        self.assertRaisesError(self.g.issue, self.sigm, self.todo, 2000)
        self.assertIsNotNone(self.g.issue(self.sigm, self.todo, 1))

    def test_list_auth(self):
        self.assertRaisesError(self.g.list_authorizations)

    def test_list_emails(self):
        self.assertRaisesError(self.g.list_emails)

    def test_list_gists(self):
        for i in None, self.sigm:
            self.assertIsNotNone(self.g.list_gists(i))

    def test_list_issues(self):
        self.assertIsNotNone(self.g.list_issues(self.sigm, self.todo))
        list_issues = self.g.list_issues
        issues = list_issues(self.sigm, self.todo, 'subscribed')
        if issues:
            self.fail('Cannot be subscribed to issues.')
        for f in ('assigned', 'created', 'mentioned'):
            self.assertIsNotNone(list_issues(self.sigm, self.todo, f))
        for s in ('open', 'closed'):
            self.assertIsNotNone(list_issues(self.sigm, self.todo, state=s))
        self.assertIsNotNone(list_issues(self.sigm, self.todo, state='closed', 
            labels='Bug,Enhancement'))
        for s in ('created', 'updated', 'comments'):
            self.assertIsNotNone(list_issues(self.sigm, self.todo, sort=s))
        for d in ('asc', 'desc'):
            self.assertIsNotNone(list_issues(self.sigm, self.todo, 
                state='closed', direction=d))
        self.assertIsNotNone(list_issues(self.sigm, self.todo, 
            since='2011-01-01T00:00:01Z'))
