"""Unit tests for the github3.pulls module."""
import pytest

from . import helper

from github3 import GitHubError
from github3 import pulls

get_pr_example_data = helper.create_example_data_helper(
    'pull_request_example'
)
get_pullreview_example_data = helper.create_example_data_helper(
    'pull_review_example'
)


url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/pulls/1347'
)

review_comment_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/pulls/1/comments'
)


class TestPullRequest(helper.UnitHelper):
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

    def test_create_review_requests(self):
        """Verify the request to ask for reviews on a PR."""
        self.instance.create_review_requests(reviewers=['sigmavirus24'])

        self.session.post.assert_called_once_with(
            url_for('requested_reviewers'),
            '{"reviewers": ["sigmavirus24"]}'
        )

    def test_create_review(self):
        """Verify the request to create a review on a PR."""
        self.instance.create_review('body', 'sha', 'APPROVED')

        self.post_called_with(
            url_for('reviews'),
            data={
                'body': 'body',
                'commit_id': 'sha',
                'event': 'APPROVED',
                'comments': [],
            }
        )

    def test_delete_review_requests(self):
        """Verify the request to cancel review requests on a PR."""
        self.instance.delete_review_requests(reviewers=['sigmavirus24'])

        self.session.delete.assert_called_once_with(
            url_for('requested_reviewers'),
            data='{"reviewers": ["sigmavirus24"]}'
        )

    def test_diff(self):
        """Show that a user can request the diff of a Pull Request."""
        self.instance.diff()

        self.session.get.assert_called_once_with(
            url_for(),
            headers={'Accept': 'application/vnd.github.diff'}
        )

    def test_is_merged_request(self):
        """Show that a user can request the merge status of a PR."""
        self.instance.merged = False
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

        self.put_called_with(
            url_for('merge'),
            data={"merge_method": "merge"}
        )

    def test_merge_squash_message(self):
        """Show that a user can merge a Pull Request."""
        self.instance.merge('commit message', merge_method='squash')

        self.put_called_with(
            url_for('merge'),
            data={"merge_method": "squash", "commit_message": "commit message"}
        )

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

    def test_review_requests(self):
        """Verify the request to fetch the review requests from a PR."""
        self.instance.review_requests()

        self.session.get.assert_called_once_with(
            url_for('requested_reviewers')
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

    def test_attributes(self):
        """Show that we extract attributes correctly."""
        assert (self.instance.merge_commit_sha ==
                'e5bd3914e2e596debea16f433f57875b5b90bcd6')
        assert not self.instance.merged
        assert self.instance.mergeable


class TestPullReview(helper.UnitHelper):
    """PullReview unit tests."""

    described_class = pulls.PullReview
    example_data = get_pullreview_example_data()

    def test_submit(self):
        """Verify the request to submit a review"""
        self.instance.submit('body', 'APPROVED')

        self.post_called_with(
            url_for('reviews/{0}/events'.format(self.instance.id)),
            data={
                'body': 'body',
                'event': 'APPROVED',
            }
        )


class TestPullRequestRequiresAuthentication(
        helper.UnitRequiresAuthenticationHelper):
    """PullRequest unit tests that demonstrate which methods require auth."""

    described_class = pulls.PullRequest
    example_data = get_pr_example_data()

    def test_close(self):
        """Show that you must be authenticated to close a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.close()

    def test_create_review_comment(self):
        """Show that you must be authenticated to close a Pull Request."""
        with pytest.raises(GitHubError):
            self.instance.create_review_comment('', '', '', 1)

    def test_create_review_requests(self):
        """Show that you must be authenticated to ask for reviews."""
        self.assert_requires_auth(self.instance.create_review_requests)

    def test_delete_review_requests(self):
        """Show that you must be authenticated to cancel review requests."""
        self.assert_requires_auth(self.instance.delete_review_requests)

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


class TestPullRequestIterator(helper.UnitIteratorHelper):
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

    def test_reviews(self):
        """Show that a user can retrieve the reviews from a Pull Request."""
        i = self.instance.reviews()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('reviews'),
            params={'per_page': 100},
            headers={}
        )


class TestReviewComment(helper.UnitHelper):
    """Unit tests for the ReviewComment class."""

    described_class = pulls.ReviewComment
    get_comment_example_data = helper.create_example_data_helper(
        'review_comment_example'
    )
    example_data = get_comment_example_data()

    def test_reply(self):
        """Verify the request to reply to a review comment."""
        self.instance.reply('foo')

        self.post_called_with(
            review_comment_url_for(),
            data={'body': 'foo', 'in_reply_to': 1}
        )

    def test_reply_requires_authentication(self):
        """Verify that a user needs to be authenticated to reply."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.reply('')


class TestPullFile(helper.UnitHelper):
    """Unit tests for the PullFile class."""

    described_class = pulls.PullFile
    get_pull_file_example_data = helper.create_example_data_helper(
        'pull_file_example'
    )
    example_data = get_pull_file_example_data()

    def test_contents(self):
        """Verify the request made to fetch a pull request file contents."""
        self.instance.contents()

        self.session.get.assert_called_once_with(
            self.example_data['contents_url']
        )


class TestPullFilePatch(TestPullFile):
    """Unit tests for the PullFile class with empty patch."""

    get_pull_file_patch_example_data = helper.create_example_data_helper(
        'pull_file_missing_patch_example'
    )
    example_data = get_pull_file_patch_example_data()
