# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Gist."""
from .helper import IntegrationHelper

import github3


class TestGist(IntegrationHelper):

    """Gist integration tests."""

    def test_comments(self):
        """Show that a user can iterate over the comments on a gist."""
        cassette_name = self.cassette_name('comments')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist(3342247)
            assert gist is not None
            for comment in gist.comments():
                assert isinstance(comment, github3.gists.comment.GistComment)

    def test_create_comment(self):
        """Show that a user can comment on a gist."""
        self.basic_login()
        cassette_name = self.cassette_name('create_comment')
        with self.recorder.use_cassette(cassette_name):
            gist = self.gh.gist('f396190a0d0047be791b')
            assert gist is not None
            c = gist.create_comment("""```ruby
            mac.split('').map.with_index do |v, i|
              positions.include?(i) ? ':' + v : v
            end
            ```""")
            assert isinstance(c, github3.gists.comment.GistComment)

    def test_commits(self):
        """Show that a user can iterate over the commits in a gist."""
        cassette_name = self.cassette_name('commits')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            gist = self.gh.gist(1834570)
            assert gist is not None
            for commit in gist.commits():
                assert isinstance(commit, github3.gists.history.GistHistory)

    def test_forks(self):
        """Show that a user can iterate over the forks of a gist."""
        cassette_name = self.cassette_name('forks')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            gist = self.gh.gist(1834570)
            assert gist is not None
            for commit in gist.forks():
                assert isinstance(commit, github3.gists.gist.Gist)
