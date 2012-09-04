import github3
from base import expect, BaseTest, str_test
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

    def test_is_member(self):
        expect(self.org.is_member(self.sigm)).isinstance(bool)

    def test_is_public_member(self):
        expect(self.org.is_public_member(self.sigm)).is_True()

    def test_list_events(self):
        ev = self.org.list_events()
        self.expect_list_of_class(ev, Event)

    def test_list_members(self):
        members = self.org.list_members()
        if members:
            self.expect_list_of_class(members, User)

    def test_list_public_members(self):
        members = self.org.list_public_members()
        if members:
            self.expect_list_of_class(members, User)

    def test_list_repos(self):
        repos = self.org.list_repos('all')
        self.expect_list_of_class(repos, Repository)

    def test_private_repos(self):
        expect(self.org.private_repos) >= 0

    def test_name(self):
        expect(self.org.name).isinstance(str_test)
        expect(self.org.name) == 'github3.py'

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.org.add_member('jcordasc', 'Collaborators')
            self.org.add_repo(self.test_repo, 'Collaborators')
            self.org.create_repo(self.test_repo + '2')
            self.org.conceal_member(self.sigm)
            self.org.create_team('New Team', permissions='pull')
            self.org.edit(name='github3[dot]py')
            self.org.list_teams()
            self.org.publicize_member(self.sigm)
            self.org.remove_member(self.sigm)
            self.org.remove_repo(self.test_repo, 'Collaborators')
            self.org.team(190083)

    def test_with_auth(self):
        if not self.auth:
            return
        # Try and do something only sigmavirus24 or other org members
        # should be able to do. As of now (26 Aug 2012) there are no other
        # org members.
        # Might as well avoid a call to the API, right?
        org = Organization(self.org.to_json(), self._g)
        try:
            expect(org.add_member('jcordasc', 'Collaborators')).is_True()
            expect(org.remove_member('jcordasc')).is_True()
        except github3.GitHubError:
            pass

        try:
            repo = self.gh3py + '/' + self.test_repo
            expect(org.add_repo(repo, 'Contributors')).is_True()
            expect(org.remove_repo(repo, 'Contributors')).is_True()
        except github3.GitHubError:
            pass

        try:
            repo = org.create_repo('test_repo_creation', 'testing')
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
            self.expect_list_of_class(teams, Team)
        except github3.GitHubError:
            pass

        try:
            expect(org.team(190083)).isinstance(Team)
        except github3.GitHubError:
            pass


class TestTeam(BaseTest):
    pass

# I have to decide how to test Teams. They're all entirely dependent upon
# being authenticated and being part of an organization.
