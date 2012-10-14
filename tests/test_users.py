from . import base
import github3
from .base import expect
from github3.users import User, Plan, Key
from github3.events import Event
from github3.repos import Repository


class TestUser(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestUser, self).__init__(methodName)
        self.user = github3.user(self.sigm)

    def test_user(self):
        expect(self.user).isinstance(User)
        expect(repr(self.user)) != ''

    def test_disk_usage(self):
        expect(self.user.disk_usage) >= 0

    def test_for_hire(self):
        with expect.raises(DeprecationWarning):
            self.user.for_hire

    def test_hireable(self):
        expect(self.user.hireable).isinstance(bool)

    def test_is_assignee_on(self):
        expect(self.user.is_assignee_on(self.sigm, self.todo)).is_True()
        expect(self.user.is_assignee_on(self.kr, 'requests')).is_False()

    def test_iter_events(self):
        expect(next(self.user.iter_events(1))).isinstance(Event)

    def test_list_events(self):
        expect(self.user.list_events()).list_of(Event)

    def test_iter_followers(self):
        expect(next(self.user.iter_followers(1))).isinstance(User)

    def test_list_followers(self):
        expect(self.user.list_followers()).list_of(User)

    def test_iter_following(self):
        expect(next(self.user.iter_following(1))).isinstance(User)

    def test_list_following(self):
        expect(self.user.list_following()).list_of(User)

    def test_iter_received_events(self):
        expect(next(self.user.iter_received_events(number=1))).isinstance(
                Event)
        expect(next(self.user.iter_received_events(True, 1))).isinstance(
                Event)

    def test_list_received_events(self):
        expect(self.user.list_received_events()).list_of(Event)
        expect(self.user.list_received_events(True)).list_of(Event)

    def test_iter_starred(self):
        expect(next(self.user.iter_starred(1))).isinstance(Repository)

    def test_list_starred(self):
        expect(self.user.list_starred()).list_of(Repository)

    def test_iter_subscriptions(self):
        expect(next(self.user.iter_subscriptions(1))).isinstance(Repository)

    def test_list_subscriptions(self):
        expect(self.user.list_subscriptions()).list_of(Repository)

    def test_owned_private_repos(self):
        expect(self.user.owned_private_repos) >= 0

    def test_total_private_gists(self):
        expect(self.user.total_private_gists) >= 0

    def test_private_gists(self):
        with expect.raises(DeprecationWarning):
            self.user.private_gists

    def test_plan(self):
        if self.user.plan:
            expect(self.user.plan).isinstance(Plan)

    def test_public_gists(self):
        expect(self.user.public_gists) >= 0

    def test_total_private_repos(self):
        expect(self.user.total_private_repos) >= 0

    def test_requires_auth(self):
        self.raisesGHE(self.user.add_email_addresses, ['foo@example.com',
                'graff@colmin.gov'])
        self.raisesGHE(self.user.delete_email_addresses, ['foo@example.com'])
        self.raisesGHE(self.user.list_org_events, self.gh3py)
        self.raisesGHE(self.user.update)

    def test_refresh(self):
        self.user.refresh()
        expect(self.user.html_url) != ''

    def test_with_auth(self):
        if not self.auth:
            return
        user = self._g.user()
        email = 'new_email@gmail.com'
        addresses = user.add_email_addresses([email])
        expect(addresses).isinstance(list)
        expect(user.delete_email_addresses([email])).is_True()
        addresses = user.add_email_address(email)
        expect(addresses).isinstance(list)
        expect(user.delete_email_address(email)).is_True()
        try:
            expect(user.list_org_events(self.gh3py)).list_of(Event)
        except github3.GitHubError:
            pass
        expect(user.update(user.name, user.email, user.blog, user.company,
            user.location, user.hireable, user.bio)).isinstance(bool)

        try:
            expect(next(user.iter_org_events(self.gh3py))).isinstance(Event)
        except github3.GitHubError:
            pass

        try:
            expect(next(user.iter_org_events(None)))
        except (github3.GitHubError, StopIteration):
            pass


class TestKey(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestKey, self).__init__(methodName)
        if self.auth:
            self.key = self._g.list_keys()[0]
        else:
            json = {
                    'url': 'https://api.github.com/user/keys/id',
                    'verified': True,
                    'id': 999999,
                    'key': 'ssh-rsa AAAAB4...',
                    'title': 'fake'
                    }
            self.key = Key(json)

    def test_key(self):
        expect(self.key).isinstance(Key)
        expect(repr(self.key)) != ''
        self.key._update_(self.key.to_json())

    def test_pubkey(self):
        expect(self.key.key).isinstance(base.str_test)

    def test_id(self):
        expect(self.key.id) > 0

    def test_title(self):
        expect(self.key.title).isinstance(base.str_test)

    def test_requires_auth(self):
        if self.auth:
            return
        self.raisesGHE(self.key.update, 'title', 'ssha-rsa AAAAB2...')
        self.raisesGHE(self.key.delete)

    def test_with_auth(self):
        if not self.auth:
            return
        expect(self.key.update(None, None)).is_False()
        expect(self.key.update(self.key.title, self.key.key)).is_True()


def TestPlan(BaseTest):
    def __init__(self, methodName='runTest'):
        self.plan = github3.users._free

    def test_plan(self):
        expect(self.plan).isinstance(Plan)
        expect(repr(self.plan)) != ''

    def test_is_free(self):
        expect(self.plan.is_free()).is_True()
