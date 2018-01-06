"""Unit tests for methods implemented on Branch."""
import github3
from . import helper

get_example_data = helper.create_example_data_helper('repos_branch_example')
url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/commits/master'
)


class TestBranch(helper.UnitHelper):
    """Branch unit tests."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_latest_sha(self):
        """Verify the request for retreiving the latest_sha."""
        headers = {
            'Accept': 'application/vnd.github.v3.sha',
            'If-None-Match': '"123"'
        }
        self.instance.latest_sha(differs_from='123')
        self.session.get.assert_called_once_with(
            url_for(),
            headers=headers
        )
