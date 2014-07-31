"""Unit tests for the github3.gists module."""
import pytest
import github3

from .helper import (create_example_data_helper, create_url_helper,
                     UnitHelper, UnitIteratorHelper)

gist_example_data = create_example_data_helper('gist_example_data')

url_for = create_url_helper(
    'https://api.github.com/gists/b4c7ac7be6e591d0d155'
)


class TestGist(UnitHelper):

    """Test regular Gist methods."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def test_create_comment(self):
        """Show that a user can create a comment."""
        self.instance.create_comment('some comment text')

        self.post_called_with(url_for('comments'),
                              data={'body': 'some comment text'})


class TestGistRequiresAuth(UnitHelper):

    """Test Gist methods which require authentication."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def after_setup(self):
        """Disable authentication."""
        self.session.has_auth.return_value = False

    def test_create_comment(self):
        """Show that a user needs to authenticate to create a comment."""
        with pytest.raises(github3.GitHubError):
            self.instance.create_comment('foo')


class TestGistIterators(UnitIteratorHelper):

    """Test Gist methods that return Iterators."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def test_comments(self):
        """Show a user can iterate over the comments on a gist."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )

    def test_commits(self):
        """Show a user can iterate over the commits on a gist."""
        i = self.instance.commits()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100},
            headers={}
        )

    def test_files(self):
        """Show that iterating over a gist's files does not make a request."""
        files = list(self.instance.files())
        assert len(files) > 0

        assert self.session.get.called is False

    def test_forks(self):
        """Show that a user can iterate over a gist's forks."""
        i = self.instance.forks()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('forks'),
            params={'per_page': 100},
            headers={}
        )
