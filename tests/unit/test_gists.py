"""Unit tests for the github3.gists module."""
import github3
import pytest

from .helper import (create_example_data_helper, create_url_helper,
                     UnitIteratorHelper)

gist_example_data = create_example_data_helper('gist_example_data')

url_for = create_url_helper(
    'https://api.github.com/gists/b4c7ac7be6e591d0d155'
)


class TestGistIterators(UnitIteratorHelper):

    """Test Gist methods that return Iterators."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    @pytest.mark.xfail
    def test_comments(self):
        """Show a user can iterate over the comments on a gist."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )
