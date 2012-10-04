import github3
from .base import expect, expect_str, BaseTest, str_test
from github3.repos import Repository
from github3.events import Event
from github3.auths import Authorization
from github3.users import Key, User
from github3.gists import Gist
from github3.issues import Issue
from github3.orgs import Organization


class TestGitHub(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGitHub, self).__init__(methodName)
        self.fake_auth = ('fake_user', 'fake_password')
        self.fake_oauth = 'foobarbogusoauth'

    def setUp(self):
        self.g = github3.GitHub()

    def test_github(self):
        expect(self.g).isinstance(github3.GitHub)
        expect_str(repr(self.g))

    def test_login(self):
        # Test "regular" auth
        self.g.login(*self.fake_auth)
        h = github3.login(*self.fake_auth)
        l = github3.GitHub(*self.fake_auth)
        for i in [self.g, h, l]:
            expect(self.fake_auth) == i._session.auth

    def test_oauth(self):
        # Test "oauth" auth
        self.g.login(token=self.fake_oauth)
        h = github3.login('', '', token=self.fake_oauth)
        for i in [self.g, h]:
            expect(i._session.headers['Authorization']) == 'token ' +\
                self.fake_oauth

    def test_gists(self):
        # My gcd example
        gist_id = 2648112
        g = self.g.gist(gist_id)
        if not g:
            self.fail('Check gcd gist')
        expect(g).isinstance(github3.gists.Gist)

        self.raisesGHE(self.g.gist, -1)

    def test_iter_gists(self):
        for user in None, self.sigm:
            expect(next(self.g.iter_gists(user))).isinstance(Gist)

    def test_list_gists(self):
        for i in None, self.sigm:
            expect(self.g.list_gists(i)).list_of(Gist)

    def test_create_gist(self):
        if not self.auth:
            return
        desc = 'Testing gist creation'
        files = {'test.txt': {'content': 'Test contents'}}
        gist = self._g.create_gist(desc, files, False)
        expect(gist).is_not_None()
        expect(gist.description) == desc
        expect(gist.is_public()).is_False()
        for g in gist.list_files():
            expect(g.content) == files[g.name]['content']
        expect(gist.delete()).is_True()

    def test_is_following(self):
        self.raisesGHE(self.g.is_following, self.sigm)

        if not self.auth:
            return

        expect(self._g.is_following(self.sigm)).isinstance(bool)

    def test_is_starred(self):
        args = (self.sigm, self.todo)

        self.raisesGHE(self.g.is_starred, *args)

        if not self.auth:
            return

        expect(self._g.is_starred(*args)).isinstance(bool)

    def test_is_subscribed(self):
        args = (self.sigm, 'github3.py')

        self.raisesGHE(self.g.is_subscribed, *args)

        if not self.auth:
            return

        expect(self._g.is_subscribed(*args)).isinstance(bool)

    def test_iter_following(self):
        expect(next(self.g.iter_following(self.kr))).isinstance(User)
        self.raisesGHE(next, self.g.iter_following())
        if not self.auth:
            return

        expect(next(self._g.iter_following())).isinstance(User)

    def test_list_following(self):
        expect(self.g.list_following(self.kr)) != []
        self.raisesGHE(self.g.list_following)

        if not self.auth:
            return

        expect(self._g.list_following()).list_of(User)

    def test_iter_followers(self):
        expect(next(self.g.iter_followers(self.kr))).isinstance(User)
        self.raisesGHE(next, self.g.iter_followers())
        if not self.auth:
            return

        expect(next(self._g.iter_followers())).isinstance(User)

    def test_list_followers(self):
        expect(self.g.list_followers(self.kr)) != []
        with expect.raises(github3.GitHubError):
            self.g.list_followers()

        if not self.auth:
            return

        expect(self._g.list_followers()).list_of(User)

    def test_iter_starred(self):
        self.raisesGHE(next, self.g.iter_starred())
        expect(next(self.g.iter_starred(self.sigm))).isinstance(Repository)
        if not self.auth:
            return

        expect(next(self._g.list_starred())).isinstance(Repository)

    def test_list_starred(self):
        self.raisesGHE(self.g.list_starred)
        expect(self.g.list_starred(self.sigm)).list_of(Repository)

        if not self.auth:
            return

        expect(self._g.list_starred()).list_of(Repository)

    def test_iter_subscribed(self):
        self.raisesGHE(next, self.g.iter_subscribed())
        expect(self.g.iter_subscribed(self.sigm)).list_of(Repository)
        if not self.auth:
            return

        expect(self._g.iter_subscribed()).list_of(Repository)

    def test_list_subscribed(self):
        self.raisesGHE(self.g.list_subscribed)
        expect(self.g.list_subscribed(self.sigm)).list_of(Repository)

        if not self.auth:
            return

        expect(self._g.list_subscribed()).list_of(Repository)

    def test_follow_unfollow(self):
        self.raisesGHE(self.g.follow, self.sigm)
        self.raisesGHE(self.g.unfollow, self.sigm)

        if not self.auth:
            return

        expect(self._g.follow(self.sigm)).isinstance(bool)
        expect(self._g.unfollow(self.sigm)).isinstance(bool)

    def test_watching(self):
        args = (self.sigm, self.todo)
        self.assertRaises(DeprecationWarning, self.g.watch, *args)
        self.assertRaises(DeprecationWarning, self.g.unwatch, *args)
        self.assertRaises(DeprecationWarning, self.g.list_watching)
        self.assertRaises(DeprecationWarning, self.g.is_watching, *args)

    def test_create_issue(self):
        title = 'Test issue for github3.py'
        self.raisesGHE(self.g.create_issue, self.sigm, self.todo, title)

        expect(self.g.create_issue(None, None, None)).is_None()

        if not self.auth:
            return

        i = self._g.create_issue(self.gh3py, self.test_repo, title,
                'Ignore this.')
        expect(i).isinstance(github3.issues.Issue)
        expect(i.close()).is_True()

    def test_issue(self):
        self.raisesGHE(self.g.issue, self.sigm, self.todo, 2000)

        i = self.g.issue(self.kr, 'requests', 1)
        self.assertIsNotNone(i)
        expect(i).isinstance(github3.issues.Issue)
        expect(self.g.issue(None, None, None)).is_None()

    def test_iter_repo_issues(self):
        with expect.raises(StopIteration):
            next(self.g.iter_repo_issues('', ''))

        expect(next(self.g.iter_repo_issues(self.kr, 'requests'))).isintance(
                Issue
                )

    def test_list_repo_issues(self):
        # Test listing issues
        list_issues = self.g.list_repo_issues
        expect(list_issues(self.kr, 'requests')) != []
        expect(list_issues(self.sigm, self.todo)).isinstance(list)
        expect(list_issues('', '')) == []

    def test_iter_user_issues(self):
        self.raisesGHE(self.g.iter_user_issues)
        if not self.auth:
            return

        expect(next(self._g.iter_user_issues())).isinstance(Issue)

    def test_list_user_issues(self):
        self.raisesGHE(self.g.list_user_issues)
        if not self.auth:
            return
        expect(self._g.list_user_issues(state='closed')).list_of(Issue)

    def test_key(self):
        self.raisesGHE(self.g.key, 2000)
        if not self.auth:
            return
        k = next(self._g.iter_keys())
        expect(self._g.key(k.id)).isinstance(Key)

    def test_keys_requires_auth(self):
        self.raisesGHE(self.g.create_key, 'Foo bar', 'bogus')
        self.raisesGHE(self.g.delete_key, 2000)
        self.raisesGHE(self.g.list_keys)

    def test_iter_repos(self):
        self.raisesGHE(next, self.g.iter_repos())
        expect(next(self.g.iter_repos(self.sigm))).isinstance(Repository)
        expect(next(self.g.iter_repos(self.sigm,
            'all'))).isinstance(Repository)
        if not self.auth:
            return

        expect(
               next(self._g.iter_repos(sort='pushed', direction='asc'))
               ).isinstance(Repository)

    def test_list_repos(self):
        self.raisesGHE(self.g.list_repos)
        expect(self.g.list_repos(self.sigm)).list_of(Repository)
        expect(self.g.list_repos(self.sigm, 'all')).list_of(Repository)
        if not self.auth:
            return
        expect(self._g.list_repos(sort='pushed', direction='asc')) != []

    def test_repository(self):
        expect(self.g.repository(self.sigm, self.todo)).isinstance(Repository)

    def test_create_repo(self):
        self.raisesGHE(self.g.create_repo, 'test_github3.py')
        if not self.auth:
            return
        r = self._g.create_repo('test.repo.creation')
        expect(r).isinstance(Repository)
        r.delete()

    def test_authorization(self):
        self.raisesGHE(self.g.authorization, 1)
        if not self.auth:
            return

        a = next(self._g.iter_authorizations())
        expect(self._g.authorization(a.id)).isinstance(Authorization)

    def test_authorize(self):
        self.raisesGHE(self.g.authorize, 'foo', 'bar', ['gist', 'user'])

    def test_iter_authorizations(self):
        self.raisesGHE(self.g.iter_authorizations)

        if not self.auth:
            return

        expect(next(self._g.iter_authorizations())).isinstance(Authorization)

    def test_list_authorizations(self):
        self.raisesGHE(self.g.list_authorizations)

        if not self.auth:
            return

        expect(self._g.list_authorizations()).list_of(Authorization)

    def test_list_emails(self):
        self.raisesGHE(self.g.list_emails)

        if self.auth:
            expect(self._g.list_emails()).list_of(str_test)

    def test_iter_emails(self):
        self.raisesGHE(self.g.iter_emails)

        if self.auth:
            expect_str(next(self._g.iter_emails()))

    def test_list_events(self):
        expect(self.g.list_events()).list_of(Event)

    def test_iter_events(self):
        expect(next(self.g.iter_events())).isinstance(Event)

    def test_iter_orgs(self):
        expect(next(self.g.iter_orgs(self.kr))).isinstance(Organization)
        self.raisesGHE(next, self.g.iter_orgs())
        if not self.auth:
            return

        expect(next(self._g.iter_orgs())).isinstance(Organization)

    def test_list_orgs(self):
        expect(self.g.list_orgs(self.kr)) != []
        self.raisesGHE(self.g.list_orgs)
        if not self.auth:
            return

        expect(self._g.list_orgs()) != []

    def test_organization(self):
        expect(self.g.organization(self.gh3py)).is_not_None()

    def test_markdown(self):
        md = "# Header\n\nParagraph\n\n## Header 2\n\nParagraph"
        reg = self.g.markdown(md)
        raw = self.g.markdown(md, raw=True)
        self.assertEqual(reg, raw)
        gfm = self.g.markdown(md, mode='gfm',
                context='sigmavirus24/github3.py')
        self.assertNotEqual(reg, gfm)

    def test_search(self):
        expect(self.g.search_issues(self.sigm, self.todo, 'closed',
                'todo')).is_not_None()
        expect(self.g.search_users(self.sigm)).is_not_None()
        expect(self.g.search_email('wynn@github.com')).is_not_None()

    def test_update_user(self):
        self.raisesGHE(self.g.update_user)
        if not self.auth:
            return
        u = self._g.user()
        expect(self._g.update_user(u.name, u.email, u.blog, u.company,
            u.location, u.hireable, u.bio)).is_True()

    def test_user(self):
        self.raisesGHE(self.g.user)
        expect(self.g.user(self.sigm)).is_not_None()

        if not self.auth:
            return

        expect(self._g.user()).isinstance(github3.users.User)

    def test_subscribe_unsub(self):
        args = (self.gh3py, self.test_repo)
        self.raisesGHE(self.g.subscribe, *args)
        self.raisesGHE(self.g.unsubscribe, *args)

        if not self.auth:
            return

        expect(self._g.subscribe(*args)).isinstance(bool)
        expect(self._g.unsubscribe(*args)).isinstance(bool)

    def test_star_unstar(self):
        args = (self.gh3py, self.test_repo)
        self.raisesGHE(self.g.star, *args)
        self.raisesGHE(self.g.unstar, *args)

        if not self.auth:
            return

        expect(self._g.star(*args)).isinstance(bool)
        expect(self._g.unstar(*args)).isinstance(bool)
