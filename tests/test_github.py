import base
import github3
from base import expect


class TestGitHub(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGitHub, self).__init__(methodName)
        self.fake_auth = ('fake_user', 'fake_password')
        self.fake_oauth = 'foobarbogusoauth'

    def test_login(self):
        # Test "regular" auth
        self.g.login(*self.fake_auth)
        h = github3.login(*self.fake_auth)
        for i in [self.g, h]:
            expect(self.fake_auth) == i._session.auth

    def test_oauth(self):
        # Test "oauth" auth
        self.g.login(token=self.fake_oauth)
        h = github3.login('', '', token=self.fake_oauth)
        for i in [self.g, h]:
            expect(i._session.headers['Authorization']) == 'token ' +\
                self.fake_oauth

        with expect.raises(github3.GitHubError):
            self.g.user()

        if self.auth:
            expect(self._g.user()).is_not_None()

    def test_gists(self):
        # My gcd example
        gist_id = 2648112
        g = self.g.gist(gist_id)
        if not g:
            self.fail('Check gcd gist')
        expect(g).isinstance(github3.gists.Gist)

        with expect.raises(github3.GitHubError):
            self.g.gist(-1)

        for i in None, self.sigm:
            expect(self.g.list_gists(i)) != []

        if self.auth:
            desc = 'Testing gist creation'
            files = {'test.txt': {'content': 'Test contents'}}
            gist = self._g.create_gist(desc, files, False)
            expect(gist).is_not_None()
            expect(gist.description) == desc
            expect(gist.is_public()).is_False()
            for g in gist.list_files():
                expect(g.content) == files[g.name]['content']
            expect(gist.delete()).is_True()

    def test_following(self):
        expect(self.g.list_followers('kennethreitz')) != []
        expect(self.g.list_following('kennethreitz')) != []
        with expect.raises(github3.GitHubError):
            self.g.is_following(self.sigm)
            self.g.follow(self.sigm)
            self.g.unfollow(self.sigm)
            self.g.list_followers()
            self.g.list_following()

        if self.auth:
            expect(self._g.is_following(self.sigm)).isinstance(bool)
            expect(self._g.follow(self.sigm)).isinstance(bool)
            expect(self._g.unfollow(self.sigm)).isinstance(bool)
            expect(self._g.list_followers()) != []
            expect(self._g.list_following()) != []

    def test_watching(self):
        expect(self.g.list_watching(self.sigm)) != []
        with expect.raises(github3.GitHubError):
            self.g.watch(self.sigm, self.todo)
            self.g.unwatch(self.sigm, self.todo)
            self.g.list_watching()
            self.g.is_watching(self.sigm, self.todo)

        if self.auth:
            expect(self._g.watch(self.sigm, self.todo)).isinstance(bool)
            expect(self._g.unwatch(self.sigm, self.todo)).isinstance(bool)
            expect(self._g.list_watching()) != []
            expect(self._g.is_watching(self.sigm, self.todo)) != []

    def test_issues(self):
        title = 'Test issue for github3.py'
        with expect.raises(github3.GitHubError):
            # Try to create one without authenticating
            self.g.create_issue(self.sigm, self.todo, title)
            # Try to get individual ones
            self.g.issue(self.sigm, self.todo, 2000)
            self.g.list_user_issues()

        i = self.g.issue(self.sigm, self.todo, 1)
        self.assertIsNotNone(i)
        expect(i).isinstance(github3.issues.Issue)
        expect(i.list_comments()) != []
        # Test listing issues
        list_issues = self.g.list_repo_issues
        expect(list_issues(self.kr, 'requests')) != []
        expect(list_issues(self.sigm, self.todo)).isinstance(list)
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
        expect(list_issues(self.sigm, self.todo,
            since='2011-01-01T00:00:01Z')).is_not_None()

        if self.auth:
            i = self._g.create_issue(self.gh3py, self.test_repo,
            'Testing github3.py', 'Ignore this.')
            expect(i).isinstance(github3.issues.Issue)
            expect(i.close()).is_True()

    def test_keys(self):
        with expect.raises(github3.GitHubError):
            self.g.create_key('Foo bar', 'bogus')
            self.g.delete_key(2000)
            self.g.get_key(2000)
            self.g.list_keys()

        # Need to find a way to make this work
        #if self.auth:
        #    k = self._g.create_key('Foo bar', 'bogus')
        #    expect(k).isinstance(github3.user.Key)

    def test_repos(self):
        with expect.raises(github3.GitHubError):
            self.g.create_repo('test_github3.py')
            self.g.list_repos()
        expect(self.g.list_repos(self.sigm)) != []
        expect(self.g.repository(self.sigm, self.todo)).is_not_None()

    def test_auths(self):
        with expect.raises(github3.GitHubError):
            self.g.list_authorizations()
            self.g.authorization(-1)
            self.g.authorize('foo', 'bar', ['gist', 'user'])

    def test_list_emails(self):
        with expect.raises(github3.GitHubError):
            self.g.list_emails()

    def test_orgs(self):
        expect(self.g.list_orgs(self.kr)) != []
        expect(self.g.organization(self.gh3py)).is_not_None()
        with expect.raises(github3.GitHubError):
            self.g.list_orgs()

    def test_markdown(self):
        md = "# Header\n\nParagraph\n\n## Header 2\n\nParagraph"
        reg = self.g.markdown(md)
        raw = self.g.markdown(md, raw=True)
        self.assertEqual(reg, raw)

    def test_search(self):
        expect(self.g.search_issues(self.sigm, self.todo, 'closed',
                'todo')).is_not_None()
        expect(self.g.search_users(self.sigm)).is_not_None()
        try:
            expect(self.g.search_email('graffatcolmingov@gmail.com')
                    ).is_not_None()
        except github3.GitHubError as err:
            if err.code == 404:
                pass
            else:
                raise err

    def test_users(self):
        with expect.raises(github3.GitHubError):
            self.g.update_user()
            self.g.user()
        expect(self.g.user(self.sigm)).is_not_None()
