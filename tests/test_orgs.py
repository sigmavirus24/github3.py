import github3
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
