"""Integration tests for methods implemented on Organization."""
import pytest

import github3
from .helper import IntegrationHelper


class TestOrganization(IntegrationHelper):

    """Organization integration tests."""

    betamax_kwargs = {"match_requests_on": ["method", "uri", "json-body"]}

    def get_organization(self, name="github3py", auth_needed=False):
        """Get the organization for each test."""
        if auth_needed:
            self.token_login()
        o = self.gh.organization(name)
        assert isinstance(o, github3.orgs.Organization)
        return o

    def get_team(self, organization, team_name="Do Not Delete"):
        """Get the desired team."""
        for team in organization.teams():
            if team.name == team_name:
                break
        else:
            assert False, f'Could not find team "{team_name}"'

        return team

    def test_add_repository(self):
        """Test the ability to add a repository to an organization."""
        self.auto_login()
        cassette_name = self.cassette_name("add_repository")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)
            assert o.add_repository("github3py/urllib3", team.id) is True

    def test_blocked_users(self):
        """Test the ability to retrieve a list of blocked users."""
        self.token_login()
        cassette_name = self.cassette_name("blocked_users")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("testgh3py")
            assert o.block("o")
            users = list(o.blocked_users())
            assert o.unblock("o")

        assert len(users) == 1
        assert ["o"] == [str(u) for u in users]

    def test_block(self):
        """Test the ability to block a user."""
        self.token_login()
        cassette_name = self.cassette_name("block")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("testgh3py")
            assert o.block("o")
            assert o.unblock("o")

    def test_unblock(self):
        """Test the ability to unblock a user."""
        self.token_login()
        cassette_name = self.cassette_name("unblock")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("testgh3py")
            assert o.block("o")
            assert o.unblock("o")

    def test_is_blocking(self):
        """Test the ability to block a user."""
        self.token_login()
        cassette_name = self.cassette_name("is_blocking")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("testgh3py")
            assert o.is_blocking("o") is False
            assert o.block("o")
            assert o.is_blocking("o")
            assert o.unblock("o")

    def test_create_project(self):
        """Test the ability to create a project in an organization."""
        self.token_login()
        cassette_name = self.cassette_name("create_org_project")
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization(name="github3py")
            r = o.create_project("test-project", body="test body")
            assert isinstance(r, github3.projects.Project)
            assert r.delete() is True

    def test_create_repository(self):
        """Test the ability to create a repository in an organization."""
        self.auto_login()
        cassette_name = self.cassette_name("create_repository")
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()
            r = o.create_repository("test-repository", description="hi")
            assert isinstance(r, github3.repos.Repository)
            assert r.delete() is True

    def test_conceal_member(self):
        """Test the ability to conceal a User's membership."""
        self.auto_login()
        cassette_name = self.cassette_name("conceal_member")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Get a public member of the organization
            public_member = next(o.public_members())
            assert isinstance(public_member, github3.users.ShortUser)

            # Conceal their membership
            assert o.conceal_member(public_member) is True
            # Re-publicize their membership
            assert o.publicize_member(public_member) is True

    def test_create_team(self):
        """Test the ability to create a new team."""
        self.auto_login()
        cassette_name = self.cassette_name("create_team")
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()

            t = o.create_team("temp-team")
            assert isinstance(t, github3.orgs.Team)
            assert t.delete() is True

    def test_create_team_child(self):
        """Test the ability to create a new child team."""
        self.auto_login()
        cassette_name = self.cassette_name("create_team_parent")
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()

            parent_t = o.create_team("temp-team", privacy="closed")
            assert isinstance(parent_t, github3.orgs.Team)

            with self.recorder.use_cassette(
                self.cassette_name("create_team_child"), **self.betamax_kwargs
            ):
                t = o.create_team("temp-team-child", parent_team_id=2589002)
                assert isinstance(parent_t, github3.orgs.Team)
                assert t.delete() is True

    def test_edit(self):
        """Test the ability to edit an organization."""
        self.auto_login()
        cassette_name = self.cassette_name("edit")
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()

            assert o.edit(location="Madison, WI") is True
            assert o.edit(description="How people build software.") is True
            assert o.edit(has_organization_projects=False) is True
            assert o.edit(has_repository_projects=False) is True
            assert o.edit(default_repository_permission="write") is True
            assert o.edit(members_can_create_repositories=False) is True

    def test_is_member(self):
        """Test the ability to check if a User is a member of the org."""
        cassette_name = self.cassette_name("is_member")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            assert o.is_member("sigmavirus24") is True

    def test_is_public_member(self):
        """Test the ability to check if a User is a public member."""
        cassette_name = self.cassette_name("is_public_member")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            assert o.is_public_member("defunkt") is False

    def test_all_events(self):
        """Test retrieving organization's complete event stream."""
        self.basic_login()
        cassette_name = self.cassette_name("all_events")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("testgh3py")

            for event in o.all_events(username="gh3test"):
                assert isinstance(event, github3.events.Event)

    def test_public_events(self):
        """Test retrieving an organization's public event stream."""
        cassette_name = self.cassette_name("public_events")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for event in o.public_events():
                assert isinstance(event, github3.events.Event)

    def test_members(self):
        """Test the ability to retrieve an organization's members."""
        self.auto_login()
        cassette_name = self.cassette_name("members")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members():
                assert isinstance(member, github3.users.ShortUser)

    @pytest.mark.xfail(
        reason="sigmavirus24 needs to actually write a test for this."
    )
    def test_can_filter_organization_members(self):
        """
        Test the ability to filter an organization's members by
        their ``"2fa_disabled"`` status. This filter is only
        available to organization owners.
        """
        self.basic_login()
        cassette_name = self.cassette_name("members_filters")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members(filter="2fa_disabled"):
                assert isinstance(member, github3.users.ShortUser)

    def test_can_filter_members_by_role(self):
        """Test the ability to filter an organization's members by role."""
        self.auto_login()
        cassette_name = self.cassette_name("members_roles")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members(role="all"):
                assert isinstance(member, github3.users.ShortUser)

    def test_project(self):
        """Test the ability to retrieve a single organization project."""
        self.token_login()
        cassette_name = self.cassette_name("project")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Grab a project, any project
            first_project = next(o.projects())

            fetched_project = o.project(first_project.id)
            assert first_project == fetched_project

    def test_projects(self):
        """Test the ability to retrieve an organization's projects."""
        self.token_login()
        cassette_name = self.cassette_name("projects")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for project in o.projects():
                assert isinstance(project, github3.projects.Project)

    def test_public_members(self):
        """Test the ability to retrieve an organization's public members."""
        self.auto_login()
        cassette_name = self.cassette_name("public_members")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.public_members():
                assert isinstance(member, github3.users.ShortUser)

    def test_repositories(self):
        """Test the ability to retrieve an organization's repositories."""
        cassette_name = self.cassette_name("repositories")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for repo in o.repositories():
                assert isinstance(repo, github3.repos.ShortRepository)

    def test_teams(self):
        """Test the ability to retrieve an organization's teams."""
        self.auto_login()
        cassette_name = self.cassette_name("teams")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for team in o.teams():
                assert isinstance(team, github3.orgs.ShortTeam)

    def test_publicize_member(self):
        """Test the ability to publicize a member of the organization."""
        self.auto_login()
        cassette_name = self.cassette_name("publicize_member")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Show that we cannot publicize someone other than the current
            # user
            with pytest.raises(github3.GitHubError):
                o.publicize_member("esacteksab")

            assert o.publicize_member("omgjlk") is True

    def test_remove_repository(self):
        """Test the ability to remove a repository from a team."""
        self.auto_login()
        cassette_name = self.cassette_name("remove_repository")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)
            assert o.remove_repository("github3py/urllib3", team.id) is True

    def test_team(self):
        """Test the ability retrieve an individual team by id."""
        self.auto_login()
        cassette_name = self.cassette_name("team")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Grab a team, any team
            first_team = next(o.teams())

            fetched_team = o.team(first_team.id)
            assert first_team == fetched_team

    def test_team_by_name(self):
        """Test the ability retrieve an individual team by name."""
        self.auto_login()
        cassette_name = self.cassette_name("team_by_name")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("erico-sandbox")

            # Grab a team, any team
            first_team = next(o.teams())

            fetched_team = o.team_by_name(first_team.slug)
            assert first_team == fetched_team

    def test_invitations(self):
        """Show that a user can retrieve an org's invites."""
        cassette_name = self.cassette_name("invitations")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("mozillatw", auth_needed=True)
            for invite in o.invitations():
                assert isinstance(invite, github3.orgs.Invitation)

    def test_invite(self):
        """Show that a user can invite a new member."""
        cassette_name = self.cassette_name("invite")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization(auth_needed=True)
            team = self.get_team(o)
            # 2354350 is gh3test
            assert o.invite(
                [team.id], invitee_id=2354350, role="direct_member"
            )

    def test_membership(self):
        """Show that a user can obtain the membership status."""
        cassette_name = self.cassette_name("membership")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("Thunderbird-client", auth_needed=True)
            assert o.membership_for("AFineOldWine")

    def test_remove_membership(self):
        """Show that a user can remove a member or invite."""
        cassette_name = self.cassette_name("remove_membership")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("Thunderbird-client", auth_needed=True)
            assert o.remove_membership("AFineOldWine")

    def test_create_hook(self):
        """Test the ability to create a hook for an organization."""
        self.token_login()
        cassette_name = self.cassette_name("create_hook")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("vogelhome", auth_needed=True)
            data = {
                "name": "web",
                "config": {
                    "url": "http://example.com/webhook",
                    "content_type": "json",
                },
            }
            hook = o.create_hook(**data)
            assert isinstance(hook, github3.orgs.OrganizationHook)

    def test_hook(self):
        """Test the ability to retrieve a hook from an organization."""
        self.token_login()
        cassette_name = self.cassette_name("hook")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("vogelhome", auth_needed=True)
            hook_id = next(o.hooks()).id
            hook = o.hook(hook_id)
        assert isinstance(hook, github3.orgs.OrganizationHook)

    def test_hooks(self):
        """Test that a user can iterate over the hooks of an organization."""
        self.basic_login()
        cassette_name = self.cassette_name("hooks")
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization("vogelhome", auth_needed=True)
            hooks = list(o.hooks())

        assert len(hooks) > 0
        for hook in hooks:
            assert isinstance(hook, github3.orgs.OrganizationHook)


class TestOrganizationHook(IntegrationHelper):

    """Integration tests for OrganizationHook object."""

    def test_delete(self):
        """Test the ability to delete a hook on an organization."""
        self.token_login()
        cassette_name = self.cassette_name("delete")
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization("vogelhome")
            hook = o.create_hook(
                "web",
                config={
                    "url": "https://httpbin.org/post",
                    "content_type": "json",
                },
            )
            deleted = hook.delete()

        assert deleted is True

    def test_edit(self):
        """Test the ability to edit a hook on an organization."""
        self.token_login()
        cassette_name = self.cassette_name("edit")
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization("vogelhome")
            hook = o.create_hook(
                "web",
                config={
                    "url": "https://httpbin.org/post",
                    "content_type": "json",
                },
            )
            data = {
                "config": {
                    "url": "https://requestb.in/15u72q01",
                    "content_type": "json",
                },
                "events": ["pull_request"],
            }
            edited = hook.edit(**data)
            hook.delete()

        assert edited

    def test_ping(self):
        """Test the ability to ping a hook on an organization."""
        self.token_login()
        cassette_name = self.cassette_name("ping")
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization("vogelhome")
            hook = o.create_hook(
                "web",
                config={
                    "url": "https://httpbin.org/post",
                    "content_type": "json",
                },
            )
            pinged = hook.ping()
            hook.delete()

        assert pinged
