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

    def test_gists(self):
        # My gcd example
        gist_id = 2648112
        if not self.g.gist(gist_id):
            self.fail('Check gcd gist')

        self.assertRaisesError(self.g.gist, -1)
        for i in None, self.sigm:
            assert self.g.list_gists(i) != []

    def test_following(self):
        self.assertRaisesError(self.g.is_following, 'sigmavirus24')
        self.assertRaisesError(self.g.follow, 'sigmavirus24')
        self.assertRaisesError(self.g.unfollow, 'sigmavirus24')
        self.assertRaisesError(self.g.list_followers)
        assert self.g.list_followers('kennethreitz') != []
        self.assertRaisesError(self.g.list_following)
        assert self.g.list_following('kennethreitz') != []

    def test_watching(self):
        sigm, todo = self.sigm, self.todo
        self.assertRaisesError(self.g.watch, sigm, todo)
        self.assertRaisesError(self.g.unwatch, sigm, todo)
        self.assertRaisesError(self.g.list_watching)
        assert self.g.list_watching(sigm) != []
        self.assertRaisesError(self.g.is_watching, sigm, todo)
        self.assertRaisesError(self.g.watch, sigm, todo)
        self.assertRaisesError(self.g.unwatch, sigm, todo)

    def test_issues(self):
        sigm, todo = self.sigm, self.todo
        title = 'Test issue for github3.py'
        # Try to create one without authenticating
        self.assertRaisesError(self.g.create_issue, sigm, todo, title)
        # Try to get individual ones
        self.assertRaisesError(self.g.issue, self.sigm, self.todo, 2000)
        self.assertIsNotNone(self.g.issue(self.sigm, self.todo, 1))
        # Test listing issues
        list_issues = self.g.list_issues
        assert list_issues(self.kr, 'requests') != []
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

    def test_keys(self):
        self.assertRaisesError(self.g.create_key, 'Foo bar', 'bogus')
        self.assertRaisesError(self.g.delete_key, 2000)
        self.assertRaisesError(self.g.get_key, 2000)
        self.assertRaisesError(self.g.list_keys)

    def test_repos(self):
        self.assertRaisesError(self.g.create_repo, 'test_github3.py')
        self.assertRaisesError(self.g.list_repos)
        assert self.g.list_repos(self.sigm) != []
        self.assertIsNotNone(self.g.repository(self.sigm, self.todo))

    def test_auths(self):
        self.assertRaisesError(self.g.list_authorizations)
        self.assertRaisesError(self.g.authorization, -1)
        self.assertRaisesError(self.g.authorize, 'foo', 'bar', ['gist',
            'user'])

    def test_list_emails(self):
        self.assertRaisesError(self.g.list_emails)

    def test_orgs(self):
        self.assertRaisesError(self.g.list_orgs)
        assert self.g.list_orgs(self.kr) != []
        self.assertIsNotNone(self.g.organization(self.gh3py))

    def test_markdown(self):
        md = "# Header\n\nParagraph\n\n## Header 2\n\nParagraph"
        reg = self.g.markdown(md)
        raw = self.g.markdown(md, raw=True)
        self.assertEqual(reg, raw)

    def test_search(self):
        self.assertIsNotNone(self.g.search_issues(self.sigm, self.todo,
            'closed', 'todo'))
        self.assertIsNotNone(self.g.search_users(self.sigm))
        self.assertIsNotNone(self.g.search_email('graffatcolmingov@gmail.com'))

    def test_users(self):
        self.assertRaisesError(self.g.update_user)
        self.assertRaisesError(self.g.user)
        self.assertIsNotNone(self.g.user(self.sigm))
