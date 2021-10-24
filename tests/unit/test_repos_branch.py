"""Unit tests for methods implemented on Branch."""
import github3
from . import helper

get_example_data = helper.create_example_data_helper("repos_branch_example")
url_for_branches = helper.create_url_helper(
    "https://api.github.com/repos/octocat/Hello-World/branches/master"
)
url_for_commits = helper.create_url_helper(
    "https://api.github.com/repos/octocat/Hello-World/commits/master"
)


class TestBranch(helper.UnitHelper):
    """Branch unit tests."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_latest_sha(self):
        """Verify the request for retreiving the latest_sha."""
        headers = {
            "Accept": "application/vnd.github.v3.sha",
            "If-None-Match": '"123"',
        }
        self.instance.latest_sha(differs_from="123")
        self.session.get.assert_called_once_with(
            url_for_commits(), headers=headers
        )

    def test_unprotect(self):
        """Verify the request to unprotect a branch."""
        self.instance.unprotect()
        self.session.delete.assert_called_once_with(
            url_for_branches("protection")
        )


class TestBranchRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit tests for Branch methods that require authentication."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_protect(self):
        """Verify that protecting a branch requires authentication."""
        self.assert_requires_auth(self.instance.protect)

    def test_unprotect(self):
        """Verify that unprotecting a branch requires authentication."""
        self.assert_requires_auth(self.instance.unprotect)
