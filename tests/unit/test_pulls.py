"""Unit tests for the github3.pulls module."""
import json
import os

from .helper import UnitHelper, UnitIteratorHelper, create_url_helper

from github3.pulls import PullRequest


def get_pr_example_data():
    """Load the example data for the PullRequest object."""
    directory = os.path.dirname(__file__)
    example = os.path.join(directory, 'pull_request_example')
    with open(example) as fd:
        data = json.load(fd)
    return data


url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/pulls/1'
)


class TestPullRequest(UnitHelper):

    """PullRequest unit tests."""

    described_class = PullRequest
    example_data = get_pr_example_data()


class TestPullRequestIterator(UnitIteratorHelper):

    """Test PullRequest methods that return Iterators."""

    described_class = PullRequest
    example_data = get_pr_example_data()

    def test_commits(self):
        """Show that a user can retrieve the commits in a Pull Request."""
        i = self.instance.commits()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100},
            headers={}
        )

    def test_issue_comments(self):
        """Show that a user can retrieve the issue-like comments on a PR."""
        i = self.instance.issue_comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments').replace('pulls', 'issues'),
            params={'per_page': 100},
            headers={}
        )

    def test_review_comments(self):
        """Show that a user can retrieve the review comments on a PR."""
        i = self.instance.review_comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )
