"""Unit tests for the github3.pulls module."""
import pytest

from .helper import (UnitHelper, UnitIteratorHelper, create_url_helper,
                     create_example_data_helper, mock)

from github3 import GitHubError
from github3 import pulls

get_pr_example_data = create_example_data_helper('pull_request_example')


url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/pulls/1'
)


class TestPullRequest(UnitHelper):
    """PullRequest unit tests."""

    described_class = pulls.PullRequest
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

    def test_create_comment(self):
        """Show that a user can comment on a PR."""
        self.instance.create_comment('body')

        self.post_called_with(
            url_for('comments').replace('pulls', 'issues'),
            data={'body': 'body'}
        )

    def test_create_review_comment(self):
        """Verify the request to create a review comment on a PR diff."""
        self.instance.create_review_comment('body', 'sha', 'path', 6)

        self.post_called_with(
            url_for('comments'),
            data={
                'body': 'body',
                'commit_id': 'sha',
                'path': 'path',
                'position': 6
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

    def test_issue(self):
        """Show that a user can retrieve the associated issue of a PR."""
        self.instance.issue()

        self.session.get.assert_called_once_with(
            url_for().replace('pulls', 'issues')
        )

    def test_merge(self):
        """Show that a user can merge a Pull Request."""
        self.instance.merge()

        self.session.put.assert_called_once_with(
	    url_for('merge'),
	    data='{"commit_message": ""}')

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

    described_class = pulls.PullRequest
    example_data = get_pr_example_data()

    def after_setup(self):
        """Make it appear as if the user has not authenticated."""
        self.session.has_auth.return_value = False

    def test_close(self):
        """Show that you must be authenticated to close a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.close()

    def test_create_review_comment(self):
        """Show that you must be authenticated to close a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.create_review_comment('', '', '', 1)

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

    described_class = pulls.PullRequest
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


class TestReviewComment(UnitHelper):
    """Unit tests for the ReviewComment class."""

    described_class = pulls.ReviewComment
    example_data = {
        "url": ("https://api.github.com/repos/octocat/Hello-World/pulls/"
                "comments/1"),
        "id": 1,
        "diff_hunk": ("@@ -16,33 +16,40 @@ public class Connection :"
                      " IConnection..."),
        "path": "file1.txt",
        "position": 1,
        "original_position": 4,
        "commit_id": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
        "original_commit_id": "9c48853fa3dc5c1c3d6f1f1cd1f2743e72652840",
        "user": {
            "login": "octocat",
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": ("https://api.github.com/users/octocat/following"
                              "{/other_user}"),
            "gists_url": ("https://api.github.com/users/octocat/gists"
                          "{/gist_id}"),
            "starred_url": ("https://api.github.com/users/octocat/starred"
                            "{/owner}{/repo}"),
            "subscriptions_url": ("https://api.github.com/users/octocat"
                                  "/subscriptions"),
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": ("https://api.github.com/users/octocat/events"
                           "{/privacy}"),
            "received_events_url": ("https://api.github.com/users/octocat"
                                    "/received_events"),
            "type": "User",
            "site_admin": False
        },
        "body": "Great stuff",
        "created_at": "2011-04-14T16:00:49Z",
        "updated_at": "2011-04-14T16:00:49Z",
        "html_url": ("https://github.com/octocat/Hello-World/pull/1"
                     "#discussion-diff-1"),
        "pull_request_url": ("https://api.github.com/repos/octocat/"
                             "Hello-World/pulls/1"),
        "_links": {
            "self": {
                "href": ("https://api.github.com/repos/octocat/Hello-World/"
                         "pulls/comments/1")
            },
            "html": {
                "href": ("https://github.com/octocat/Hello-World/pull/1"
                         "#discussion-diff-1")
            },
            "pull_request": {
                "href": ("https://api.github.com/repos/octocat/"
                         "Hello-World/pulls/1")
            }
        }
    }

    def test_reply(self):
        """Verify the request to reply to a review comment."""
        self.instance.reply('foo')

        self.post_called_with(
            url_for('comments'),
            data={'body': 'foo', 'in_reply_to': '1'}
        )

    def test_reply_requires_authentication(self):
        """Verify that a user needs to be authenticated to reply."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.reply('')


class TestPullFile(UnitHelper):
    """Unit tests for the PullFile class."""

    described_class = pulls.PullFile
    example_data = {
        "sha": "bbcd538c8e72b8c175046e27cc8f907076331401",
        "filename": "file1.txt",
        "status": "added",
        "additions": 103,
        "deletions": 21,
        "changes": 124,
        "blob_url": ("https://github.com/octocat/Hello-World/blob/"
                     "6dcb09b5b57875f334f61aebed695e2e4193db5e/file1.txt"),
        "raw_url": ("https://github.com/octocat/Hello-World/raw/"
                    "6dcb09b5b57875f334f61aebed695e2e4193db5e/file1.txt"),
        "contents_url": ("https://api.github.com/repos/octocat/Hello-World/"
                         "contents/file1.txt?ref=6dcb09b5b57875f334f61aebed"
                         "695e2e4193db5e"),
        "patch": ("@@ -132,7 +132,7 @@ module Test @@ -1000,7 +1000,7 @@"
                  " module Test")
    }

    def test_contents(self):
        """Verify the request made to fetch a pull request file contents."""
        self.instance.contents()

        self.session.get.assert_called_once_with(
            self.example_data['contents_url']
        )
