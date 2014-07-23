import github3
from tests.utils import BaseCase, load


class TestTeam(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestTeam, self).__init__(methodName)
        self.team = github3.orgs.Team(load('team'))
        self.api = "https://api.github.com/teams/190009"

    def setUp(self):
        super(TestTeam, self).setUp()
        self.team = github3.orgs.Team(self.team.to_json(), self.g)

    def test_repr(self):
        assert repr(self.team).startswith('<Team')

    def test_equality(self):
        t = github3.orgs.Team(load('team'))
        assert self.team == t
        t._uniq = 'foo'
        assert self.team != t


class TestOrganization(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestOrganization, self).__init__(methodName)
        self.org = github3.orgs.Organization(load('org'))
        self.api = "https://api.github.com/orgs/github3py"

    def setUp(self):
        super(TestOrganization, self).setUp()
        self.org = github3.orgs.Organization(self.org.to_json(), self.g)

    def test_repr(self):
        assert repr(self.org).startswith('<Organization ')

    def test_set_type(self):
        json = self.org.to_json().copy()
        del json['type']
        o = github3.orgs.Organization(json)
        assert o.type == 'Organization'

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

        self.assertRaises(github3.GitHubError, self.org.edit)

        self.login()
        assert self.org.edit() is False
        self.not_called()

        assert self.org.edit('foo', 'foo', 'foo', 'foo', 'foo')
        self.mock_assertions()

    def test_is_member(self):
        self.response('', 404)
        self.get(self.api + '/members/user')

        assert self.org.is_member('user') is False
        self.mock_assertions()

    def test_is_public_member(self):
        self.response('', 204)
        self.get(self.api + '/public_members/user')

        assert self.org.is_public_member('user') is True
        self.mock_assertions()

    def test_publicize_member(self):
        self.response('', 204)
        self.put(self.api + '/public_members/user')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.org.publicize_member, None)

        self.login()
        assert self.org.publicize_member('user')
        self.mock_assertions()

    def test_remove_member(self):
        self.response('', 404)
        self.delete(self.api + '/members/user')

        self.assertRaises(github3.GitHubError, self.org.remove_member, None)

        self.not_called()
        self.login()
        assert self.org.remove_member('user') is False
        self.mock_assertions()

    def test_team(self):
        self.response('team')
        self.get(self.github_url + 'teams/1')

        self.assertRaises(github3.GitHubError, self.org.team, 0)

        self.login()
        assert self.org.team(-1) is None
        self.not_called()

        assert isinstance(self.org.team(1), github3.orgs.Team)
        self.mock_assertions()

    def test_equality(self):
        assert self.org == github3.orgs.Organization(load('org'))
