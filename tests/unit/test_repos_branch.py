"""Unit tests for methods implemented on Branch."""
import github3
from . import helper

get_example_data = helper.create_example_data_helper('repos_branch_example')
url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/commits/master'
)
protection_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/branches/master/protection'
)


class TestBranch(helper.UnitHelper):
    """Branch unit tests."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_latest_sha(self):
        """Verify the request for retreiving the latest_sha."""
        headers = {
            'Accept': 'application/vnd.github.chitauri-preview+sha',
            'If-None-Match': '"123"'
        }
        self.instance.latest_sha(differs_from='123')
        self.session.get.assert_called_once_with(
            url_for(),
            headers=headers
        )

    def test_protection_full(self):
        """Verify the request for retrieving the full
        protection config for a branch."""
        headers = {
            'Accept': 'application/vnd.github.loki-preview+json',
        }
        self.instance.protection_full()
        self.session.get.assert_called_once_with(
            protection_url_for(),
            headers=headers,
        )
