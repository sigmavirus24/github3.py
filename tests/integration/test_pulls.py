# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on PullRequest."""

import github3

from .helper import IntegrationHelper


class TestPullRequest(IntegrationHelper):

    """PullRequest integration tests."""

    def get_pull_request(self, repository='sigmavirus24/github3.py', num=235):
        """Get the pull request we wish to use in this test."""
        owner, repo = repository.split('/')
        p = self.gh.pull_request(owner, repo, num)
        assert isinstance(p, github3.pulls.PullRequest)
        return p

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


class TestReviewComment(IntegrationHelper):

    """Integration tests for the ReviewComment object."""

    def test_reply(self):
        """Show that a user can reply to an existing ReviewComment."""
        self.basic_login()
        cassette_name = self.cassette_name('reply')
        with self.recorder.use_cassette(cassette_name):
            p = self.gh.pull_request('sigmavirus24', 'github3.py', 286)
            c = next(p.review_comments())
            comment = c.reply('Replying to comments is fun.')
        assert isinstance(comment, github3.pulls.ReviewComment)
