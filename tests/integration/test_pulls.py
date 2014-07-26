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

    def test_issue_comments(self):
        """Show that one can iterate over a PRs issue comments."""
        cassette_name = self.cassette_name('issue_comments')
        with self.recorder.use_cassette(cassette_name):
            p = self.get_pull_request()
            for comment in p.issue_comments():
                assert isinstance(comment,
                                  github3.issues.comment.IssueComment)
