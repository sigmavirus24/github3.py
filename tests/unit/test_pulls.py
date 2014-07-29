"""Unit tests for the github3.pulls module."""
import json
import os
import pytest

from .helper import UnitHelper, UnitIteratorHelper, create_url_helper

from github3 import GitHubError
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

    def test_close(self):
        """Show that a user can close a Pull Request."""
        self.instance.close()

        self.patch_called_with(
            url_for(),
            data={
                'title': self.instance.title,
                'body': self.instance.body,
                'state': 'closed'
            }
        )

    def test_diff(self):
        """Show that a user can request the diff of a Pull Request."""
        self.instance.diff()

        self.session.get.assert_called_once_with(
            url_for(),
            headers={'Accept': 'application/vnd.github.diff'}
        )

    def test_is_merged(self):
        """Show that a user can request the merge status of a PR."""
        self.instance.is_merged()

        self.session.get.assert_called_once_with(url_for('merge'))

    def test_merge(self):
        """Show that a user can merge a Pull Request."""
        self.instance.merge()

        self.session.put.assert_called_once_with(url_for('merge'), data=None)

    def test_patch(self):
        """Show that a user can fetch the patch from a Pull Request."""
        self.instance.patch()

        self.session.get.assert_called_once_with(
            url_for(),
            headers={'Accept': 'application/vnd.github.patch'}
        )

    def test_reopen(self):
        """Show that a user can reopen a Pull Request that was closed."""
        self.instance.reopen()

        self.patch_called_with(
            url_for(),
            data={
                'title': self.instance.title,
                'body': self.instance.body,
                'state': 'open'
            }
        )

    def test_update(self):
        """Show that a user can update a Pull Request."""
        self.instance.update('my new title',
                             'my new body',
                             'open')

        self.patch_called_with(
            url_for(),
            data={
                'title': 'my new title',
                'body': 'my new body',
                'state': 'open'
            }
        )


class TestPullRequestRequiresAuthentication(UnitHelper):

    """PullRequest unit tests that demonstrate which methods require auth."""

    described_class = PullRequest
    example_data = get_pr_example_data()

    def after_setup(self):
        """Make it appear as if the user has not authenticated."""
        self.session.has_auth.return_value = False

    def test_close(self):
        """Show that you must be authenticated to close a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.close()

    def test_merge(self):
        """Show that you must be authenticated to merge a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.merge()

    def test_reopen(self):
        """Show that you must be authenticated to reopen a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.reopen()

    def test_update(self):
        """Show that you must be authenticated to update a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.update('foo', 'bar', 'bogus')


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

    def test_files(self):
        """Show that a user can retrieve the files from a Pull Request."""
        i = self.instance.files()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('files'),
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
