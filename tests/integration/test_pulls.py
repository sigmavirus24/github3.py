# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on PullRequest."""
import github3
from github3 import repos

from .helper import IntegrationHelper


class TestPullRequest(IntegrationHelper):
    """PullRequest integration tests."""

    def get_pull_request(self, repository='sigmavirus24/github3.py', num=235):
        """Get the pull request we wish to use in this test."""
        owner, repo = repository.split('/')
        p = self.gh.pull_request(owner, repo, num)
        assert isinstance(p, github3.pulls.PullRequest)
        return p

    def test_close(self):
        """Show that one can close an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('close')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(
                repository='github3py/delete_contents',
                num=2,
            )
            assert p.close() is True

    def test_create_comment(self):
        """Show that a user can create a comment on a PR."""
        self.basic_login()
        cassette_name = self.cassette_name('create_comment')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=423)
            comment = p.create_comment('Testing pull request comment')
        assert isinstance(comment, github3.issues.comment.IssueComment)

    def test_commits(self):
        """Show that one can iterate over a PR's commits."""
        cassette_name = self.cassette_name('commits')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for commit in p.commits():
                assert isinstance(commit, github3.repos.commit.ShortCommit)

    def test_create_review_comment(self):
        """Show that a user can create an in-line reveiw comment on a PR."""
        self.basic_login()
        cassette_name = self.cassette_name('create_review_comment')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=286)
            comment = p.create_review_comment(
                body='Testing review comments',
                commit_id='4437428aefdb50913e2acabd0552bd13021dc38f',
                path='github3/pulls.py',
                position=6
            )
        assert isinstance(comment, github3.pulls.ReviewComment)

    def test_create_review_requests(self):
        """Show that a user can create review requests on a PR."""
        self.token_login()
        cassette_name = self.cassette_name('create_review_requests')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=873)
            pull_request = p.create_review_requests(reviewers=['sigmavirus24'])
        assert isinstance(pull_request, github3.pulls.ShortPullRequest)

    def test_create_review(self):
        """Verify the request to create a pending review on a PR."""
        self.token_login()
        cassette_name = self.cassette_name('create_review')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=819)
            comment = p.create_review(
                body='Testing create review',
                event='COMMENT',
            )
        assert isinstance(comment, github3.pulls.PullReview)

    def test_delete_review_requests(self):
        """Show that a user can delete review requests on a PR."""
        self.token_login()
        cassette_name = self.cassette_name('delete_review_requests')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=873)
            assert p.delete_review_requests(reviewers=['sigmavirus24']) is True

    def test_diff(self):
        """Show that one can retrieve a bytestring diff of a PR."""
        cassette_name = self.cassette_name('diff')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            diff = p.diff()
            assert isinstance(diff, bytes)
            assert len(diff) > 0

    def test_files(self):
        """Show that one can iterate over a PR's files."""
        cassette_name = self.cassette_name('files')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for pr_file in p.files():
                assert isinstance(pr_file, github3.pulls.PullFile)

    def test_is_merged(self):
        """Show that one can check if a PR was merged."""
        cassette_name = self.cassette_name('is_merged')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            assert p.is_merged() is True

    def test_issue(self):
        """Show that one can retrieve the associated issue of a PR."""
        cassette_name = self.cassette_name('issue')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            issue = p.issue()
            assert isinstance(issue, github3.issues.Issue)

    def test_issue_comments(self):
        """Show that one can iterate over a PR's issue comments."""
        cassette_name = self.cassette_name('issue_comments')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for comment in p.issue_comments():
                assert isinstance(comment,
                                  github3.issues.comment.IssueComment)

    def test_patch(self):
        """Show that a user can get the patch from a PR."""
        cassette_name = self.cassette_name('patch')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            patch = p.patch()
            assert isinstance(patch, bytes)
            assert len(patch) > 0

    def test_pull_reviews(self):
        """Show that one can iterate over a PR's reviews."""
        cassette_name = self.cassette_name('pull_reviews')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=671)
            for pull_review in p.reviews():
                assert isinstance(pull_review, github3.pulls.PullReview)
                assert isinstance(pull_review.user, github3.users.ShortUser)

    def test_reopen(self):
        """Show that one can reopen an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('reopen')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(
                repository='github3py/delete_contents',
                num=2,
            )
            assert p.reopen() is True

    def test_review_comments(self):
        """Show that one can iterate over a PR's review comments."""
        cassette_name = self.cassette_name('review_comments')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for comment in p.review_comments():
                assert isinstance(comment, github3.pulls.ReviewComment)

    def test_review_requests(self):
        """Show that one can retrieve the review requests of a PR."""
        cassette_name = self.cassette_name('review_requests')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(num=873)
            review_requests = p.review_requests()
        assert isinstance(review_requests, github3.pulls.ReviewRequests)

    def test_update(self):
        """Show that one can update an open Pull Request."""
        self.basic_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request(
                repository='github3py/delete_contents',
                num=2,
            )
            assert p.update(p.title) is True

    def test_repository(self):
        """Show that the pull request has the owner repository."""
        self.basic_login()
        cassette_name = self.cassette_name('single')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            assert isinstance(p.repository, github3.repos.ShortRepository)


class TestPullReview(IntegrationHelper):
    """Integration tests for the PullReview object."""

    def test_submit(self):
        self.token_login()
        cassette_name = self.cassette_name('submit')
        with self.recorder.use_cassette(cassette_name):
            pr = self.gh.pull_request("sigmavirus24", "github3.py", 819)
            p = pr.create_review(
                body='Testing submit review',
            )
            p.submit(
                body='Testing submit review',
                event='COMMENT',
            )
        assert p.submitted_at is not None


class TestReviewComment(IntegrationHelper):
    """Integration tests for the ReviewComment object."""

    def test_reply(self):
        """Show that a user can reply to an existing ReviewComment."""
        self.basic_login()
        cassette_name = self.cassette_name('reply')
        with self.recorder.use_cassette(cassette_name):
            p = self.gh.pull_request('github3py', 'delete_contents', 2)
            c = next(p.review_comments())
            comment = c.reply('Replying to comments is fun.')
        assert isinstance(comment, github3.pulls.ReviewComment)


class TestPullFile(IntegrationHelper):
    """Integration tests for the PullFile object."""

    def get_pull_request_file(self, owner, repo, pull_number, filename):
        """Helper method to retrieve a PR file."""
        p = self.gh.pull_request(owner, repo, pull_number)

        for pull_file in p.files():
            if pull_file.filename == filename:
                break
        else:
            assert False, "Could not find '{0}'".format(filename)

        return pull_file

    def test_contents(self):
        """Show that a user can retrieve the contents of a PR file."""
        cassette_name = self.cassette_name('contents')
        with self.recorder.use_cassette(cassette_name):
            pull_file = self.get_pull_request_file(
                owner='sigmavirus24', repo='github3.py', pull_number=286,
                filename='github3/pulls.py'
            )
            contents = pull_file.contents()
            assert isinstance(contents, repos.contents.Contents)
            assert contents.decoded != b''
