import pytest

import github3

from github3 import GitHubError
from github3.users import User

from .helper import (UnitHelper, UnitIteratorHelper, create_url_helper,
                     create_example_data_helper)

url_for = create_url_helper(
    'https://api.github.com/users/esacteksab'
)

get_user_example_data = create_example_data_helper('user_example_data')


class TestUserIterators(UnitIteratorHelper):

    """Test User methods that return iterators."""

    described_class = github3.users.User

    def test_followers(self):
        """Test the request to retrieve follwers."""
        f = self.instance.followers()
        self.get_next(f)

        self.session.get.assert_called_once_with(
            url_for('followers'),
            params={'per_page': 100},
            headers={}
        )
