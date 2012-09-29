import github3
from .base import expect, BaseTest, str_test
from github3.orgs import Organization, Team
from github3.events import Event
from github3.users import User
from github3.repos import Repository


class TestOrganization(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestOrganization, self).__init__(methodName)
        self.org = self.g.organization(self.gh3py)

    def test_organization(self):
        expect(self.org).isinstance(Organization)
        expect(repr(self.org)) != ''
        self.org._update_(self.org.to_json())

    def test_is_member(self):
        expect(self.org.is_member(self.sigm)).isinstance(bool)

    def test_is_public_member(self):
        expect(self.org.is_public_member(self.sigm)).is_True()

    def test_iter_events(self):
        expect(self.org.iter_events().next()).isinstance(Event)

    def test_list_events(self):
        expect(self.org.list_events()).list_of(Event)

    def test_iter_members(self):
        members = [m for m in self.org.iter_members()]
        expect(members).list_of(User)

    def test_list_members(self):
        expect(self.org.list_members()).list_of(User)

    def test_iter_public_members(self):
        members = [m for m in self.org.iter_public_members()]
        expect(members).list_of(User)

    def test_list_public_members(self):
        expect(self.org.list_public_members()).list_of(User)

    def test_iter_repos(self):
        repos = [r for r in self.org.iter_repos()]
        expect(repos).list_of(Repository)

    def test_list_repos(self):
        repos = self.org.list_repos('all')
        self.expect_list_of_class(repos, Repository)

    def test_private_repos(self):
        expect(self.org.private_repos) >= 0

    def test_name(self):
        expect(self.org.name).isinstance(str_test)
        expect(self.org.name) == 'github3.py'

    def test_requires_auth(self):
        self.raisesGHE(self.org.add_member, 'gh3test', 'Collaborators')
        self.raisesGHE(self.org.add_repo, self.test_repo, 'Collaborators')
        self.raisesGHE(self.org.create_repo, self.test_repo + '2')
        self.raisesGHE(self.org.conceal_member, self.sigm)
        self.raisesGHE(self.org.create_team, 'New Team', permissions='pull')
        self.raisesGHE(self.org.edit, name='github3[dot]py')
        self.raisesGHE(self.org.list_teams)
        self.raisesGHE(self.org.publicize_member, self.sigm)
        self.raisesGHE(self.org.remove_member, self.sigm)
        self.raisesGHE(self.org.remove_repo, self.test_repo, 'Collaborators')
        self.raisesGHE(self.org.team, 190083)

    def test_with_auth(self):
        if not self.auth:
            return
        # Try and do something only sigmavirus24 or other org members
        # should be able to do. As of now (26 Aug 2012) there are no other
        # org members.
        # Might as well avoid a call to the API, right?
        org = Organization(self.org.to_json(), self._g)
        try:
            expect(org.add_member('gh3test', 'Collaborators')).is_True()
            expect(org.remove_member('gh3test')).is_True()
        except github3.GitHubError:
            pass

        try:
            repo = self.gh3py + '/' + self.test_repo
            expect(org.add_repo(repo, 'Contributors')).is_True()
            expect(org.remove_repo(repo, 'Contributors')).is_True()
        except github3.GitHubError:
            pass

        try:
            repo = org.create_repo('test_repo_creation', 'testing',
                    team_id=190083)
            expect(repo).isinstance(Repository)
            repo.delete()
        except github3.GitHubError:
            pass

        try:
            expect(org.conceal_member(self.sigm)).is_True()
            expect(org.publicize_member(self.sigm)).is_True()
        except github3.GitHubError:
            pass

        try:
            team = org.create_team('New Team', permissions='admin')
            expect(team).isinstance(Team)
            team.delete()
        except github3.GitHubError:
            pass

        try:
            expect(org.edit(name='github3[dot]py')).is_True()
            expect(org.edit(name='github3.py')).is_True()
        except github3.GitHubError:
            pass

        try:
            teams = org.list_teams()
            expect(teams).list_of(Team)
        except github3.GitHubError:
            pass

        try:
            expect(org.iter_teams().next()).isinstance(Team)
        except github3.GitHubError:
            pass

        try:
            expect(org.team(190083)).isinstance(Team)
        except github3.GitHubError:
            pass

        try:
            expect(org.add_member(self.sigm, 'Foo')).is_False()
        except github3.GitHubError:
            pass

        try:
            expect(org.add_repo(self.test_repo, 'Foo')).is_False()
        except github3.GitHubError:
            pass

        try:
            co = org.company
            em = org.email
            loc = org.location
            name = org.name
            expect(org.edit()).is_False()
            expect(org.edit(None, 'github3.io', em, loc, name)).is_True()
            expect(org.edit(None, co, em, loc, name)).is_True()
        except github3.GitHubError:
            pass

        try:
            expect(org.remove_repo(self.test_repo, 'Foo')).isinstance(bool)
        except github3.GitHubError:
            pass


class TestTeam(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestTeam, self).__init__(methodName)
        if self.auth:
            org = self._g.organization(self.gh3py)
            self.team = org.team(190083)
        else:
            team = {'url': 'https://api.github.com/teams/190083',
                    'permission': 'pull', 'name': 'Collaborators',
                    'id': 190083}
            self.team = Team(team)

    def test_team(self):
        expect(self.team).isinstance(Team)
        expect(repr(self.team)) != ''
        self.team._update_(self.team.to_json())

    def test_edit(self):
        if self.auth:
            expect(self.team.edit(None)).is_False()
            expect(self.team.edit('Collabs')).is_True()
            expect(self.team.edit('Collaborators')).is_True()
        else:
            self.raisesGHE(self.team.edit, None)

    def test_has_repo(self):
        expect(self.team.has_repo('github3.py')).isinstance(bool)

    def test_is_member(self):
        expect(self.team.is_member(self.sigm)).isinstance(bool)

    def test_iter_members(self):
        if not self.auth:
            return
        members = [m for m in self.team.iter_members()]
        expect(members).list_of(User)

    def test_list_members(self):
        if not self.auth:
            return
        expect(self.team.list_members()).list_of(User)

    def test_iter_repos(self):
        if not self.auth:
            return
        repos = [r for r in self.team.iter_repos()]
        expect(repos).isinstance(Repository)

    def test_list_repos(self):
        if not self.auth:
            return
        expect(self.team.list_repos()).list_of(Repository)

    def test_remove_member(self):
        if self.auth:
            expect(self.team.remove_member(self.sigm)).is_True()
        else:
            self.raisesGHE(self.team.remove_member, self.sigm)

    def test_remove_repo(self):
        if self.auth:
            expect(self.team.remove_repo(self.test_repo)).isinstance(bool)
        else:
            self.raisesGHE(self.team.remove_repo, self.test_repo)
