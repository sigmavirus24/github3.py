import github3
from mock import patch, Mock
from tests.utils import BaseCase, load, expect


class TestTeam(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestTeam, self).__init__(methodName)
        self.team = github3.orgs.Team(load('team'))
        self.api = "https://api.github.com/teams/190009"

    def setUp(self):
        super(TestTeam, self).setUp()
        self.team = github3.orgs.Team(self.team.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.team).startswith('<Team')).is_True()

    def test_equality(self):
        t = github3.orgs.Team(load('team'))
        expect(self.team) == t
        t.id = 'foo'
        expect(self.team) != t

    def test_add_member(self):
        self.response('', 204)
        self.put(self.api + '/members/foo')
        self.conf = {'data': None}

        with expect.githuberror():
            self.team.add_member('foo')

        self.not_called()
        self.login()
        expect(self.team.add_member('foo')).is_True()
        self.mock_assertions()

    def test_add_repo(self):
        self.response('', 204)
        self.put(self.api + '/repos/repo')
        self.conf = {'data': None}

        with expect.githuberror():
            self.team.add_repo('repo')

        self.not_called()
        self.login()
        expect(self.team.add_repo('repo')).is_True()
        self.mock_assertions()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.team.delete()

        self.not_called()
        self.login()
        expect(self.team.delete()).is_True()
        self.mock_assertions()

    def test_edit(self):
        self.response('team', 200)
        self.patch(self.api)
        self.conf = {'data': {'name': 'Collab', 'permission': 'admin'}}

        with expect.githuberror():
            self.team.edit(None)

        self.login()
        expect(self.team.edit(None)).is_False()
        self.not_called()

        expect(self.team.edit('Collab', 'admin')).is_True()
        self.mock_assertions()

    def test_has_repo(self):
        self.response('', 204)
        self.get(self.api + '/repos/repo')

        expect(self.team.has_repo('repo')).is_True()
        self.mock_assertions()

    def test_is_member(self):
        self.response('', 404)
        self.get(self.api + '/members/user')

        expect(self.team.is_member('user')).is_False()
        self.mock_assertions()

    def test_iter_members(self):
        self.response('user', _iter=True)
        self.get(self.api + '/members')

        expect(next(self.team.iter_members())).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_repos(self):
        self.response('repo', _iter=True)
        self.get(self.api + '/repos')

        expect(next(self.team.iter_repos())).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

    def test_remove_member(self):
        self.response('', 204)
        self.delete(self.api + '/members/user')

        with expect.githuberror():
            self.team.remove_member(None)

        self.not_called()
        self.login()
        expect(self.team.remove_member('user')).is_True()
        self.mock_assertions()

    def test_remove_repo(self):
        self.response('', 204)
        self.delete(self.api + '/repos/repo')

        with expect.githuberror():
            self.team.remove_repo(None)

        self.not_called()
        self.login()
        expect(self.team.remove_repo('repo')).is_True()
        self.mock_assertions()


class TestOrganization(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestOrganization, self).__init__(methodName)
        self.org = github3.orgs.Organization(load('org'))
        self.api = "https://api.github.com/orgs/github3py"

    def setUp(self):
        super(TestOrganization, self).setUp()
        self.org = github3.orgs.Organization(self.org.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.org).startswith('<Organization ')).is_True()

    def test_set_type(self):
        json = self.org.to_json().copy()
        del json['type']
        o = github3.orgs.Organization(json)
        expect(o.type) == 'Organization'

    def test_add_member(self):
        with expect.githuberror():
            self.org.add_member(None, None)

        self.login()
        with patch.object(github3.orgs.Organization, 'iter_teams') as it:
            it.return_value = iter([])
            expect(self.org.add_member('foo', 'bar')).is_False()
            team = Mock()
            team.name = 'bar'
            team.add_member.return_value = True
            it.return_value = iter([team])
            expect(self.org.add_member('foo', 'bar')).is_True()
            team.add_member.assert_called_once_with('foo')

    def test_add_repo(self):
        with expect.githuberror():
            self.org.add_repo(None, None)

        self.login()
        with patch.object(github3.orgs.Organization, 'iter_teams') as it:
            it.return_value = iter([])
            expect(self.org.add_repo('foo', 'bar')).is_False()
            team = Mock()
            team.name = 'bar'
            team.add_repo.return_value = True
            it.return_value = iter([team])
            expect(self.org.add_repo('foo', 'bar')).is_True()
            team.add_repo.assert_called_once_with('foo')

    def test_create_repo(self):
        self.response('repo', 201)
        self.post(self.api + '/repos')
        self.conf = {
            'data': {
                'name': 'repo',
                'description': 'desc',
                'homepage': '',
                'private': False,
                'has_issues': True,
                'has_wiki': True,
                'has_downloads': True,
                'auto_init': False,
                'team_id': 1,
                'gitignore_template': '',
            }
        }

        with expect.githuberror():
            self.org.create_repo(None)

        self.not_called()
        self.login()
        expect(self.org.create_repo('repo', 'desc', team_id=1)).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

    def test_conceal_member(self):
        self.response('', 204)
        self.delete(self.api + '/public_members/user')

        with expect.githuberror():
            self.org.conceal_member(None)

        self.not_called()
        self.login()
        expect(self.org.conceal_member('user')).is_True()
        self.mock_assertions()

    def test_create_team(self):
        self.response('team', 201)
        self.post(self.api + '/teams')
        self.conf = {
            'data': {
                'name': 'team',
                'repo_names': [],
                'permissions': 'push'
            }
        }

        with expect.githuberror():
            self.org.create_team(None)

        self.not_called()
        self.login()
        expect(self.org.create_team('team', permissions='push')).isinstance(
            github3.orgs.Team)
        self.mock_assertions()

    def test_edit(self):
        self.response('org', 200)
        self.patch(self.api)
        self.conf = {
            'data': {
                'billing_email': 'foo',
                'company': 'foo',
                'email': 'foo',
                'location': 'foo',
                'name': 'foo',
            }
        }

        with expect.githuberror():
            self.org.edit()

        self.login()
        expect(self.org.edit()).is_False()
        self.not_called()

        expect(self.org.edit('foo', 'foo', 'foo', 'foo', 'foo')).is_True()
        self.mock_assertions()

    def test_is_member(self):
        self.response('', 404)
        self.get(self.api + '/members/user')

        expect(self.org.is_member('user')).is_False()
        self.mock_assertions()

    def test_is_public_member(self):
        self.response('', 204)
        self.get(self.api + '/public_members/user')

        expect(self.org.is_public_member('user')).is_True()
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get(self.api + '/events')

        expect(next(self.org.iter_events())).isinstance(github3.events.Event)
        self.mock_assertions()

    def test_iter_members(self):
        self.response('user', _iter=True)
        self.get(self.api + '/members')

        expect(next(self.org.iter_members())).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_public_members(self):
        self.response('user', _iter=True)
        self.get(self.api + '/public_members')

        expect(next(self.org.iter_public_members())).isinstance(
            github3.users.User)
        self.mock_assertions()

    def test_iter_repos(self):
        self.response('repo', _iter=True)
        self.get(self.api + '/repos')
        self.conf = {'params': {}}

        expect(next(self.org.iter_repos())).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

        expect(next(self.org.iter_repos('foo'))).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

        self.conf['params'] = {'type': 'all'}
        expect(next(self.org.iter_repos('all'))).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

    def test_iter_teams(self):
        self.response('team', _iter=True)
        self.get(self.api + '/teams')

        with expect.githuberror():
            self.org.iter_teams()

        self.not_called()
        self.login()
        expect(next(self.org.iter_teams())).isinstance(github3.orgs.Team)
        self.mock_assertions()

    def test_publicize_member(self):
        self.response('', 204)
        self.put(self.api + '/public_members/user')
        self.conf = {}

        with expect.githuberror():
            self.org.publicize_member(None)

        self.not_called()
        self.login()
        expect(self.org.publicize_member('user')).is_True()
        self.mock_assertions()

    def test_remove_member(self):
        self.response('', 404)
        self.delete(self.api + '/members/user')

        with expect.githuberror():
            self.org.remove_member(None)

        self.not_called()
        self.login()
        expect(self.org.remove_member('user')).is_False()
        self.mock_assertions()

    def test_remove_repo(self):
        with expect.githuberror():
            self.org.remove_repo(None, None)

        self.login()
        with patch.object(github3.orgs.Organization, 'iter_teams') as it:
            it.return_value = iter([])
            expect(self.org.remove_repo('foo', 'bar')).is_False()
            team = Mock()
            team.name = 'bar'
            team.remove_repo.return_value = True
            it.return_value = iter([team])
            expect(self.org.remove_repo('foo', 'bar')).is_True()
            team.remove_repo.assert_called_once_with('foo')

    def test_team(self):
        self.response('team')
        self.get(self.github_url + 'teams/1')

        with expect.githuberror():
            self.org.team(0)

        self.login()
        expect(self.org.team(-1)).is_None()
        self.not_called()

        expect(self.org.team(1)).isinstance(github3.orgs.Team)
        self.mock_assertions()

    def test_equality(self):
        expect(self.org) == github3.orgs.Organization(load('org'))
