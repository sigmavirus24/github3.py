"""Unit tests for the Issue class."""
import github3
import pytest

from github3.issues.label import Label
from .helper import create_example_data_helper
from .helper import UnitHelper
from .helper import create_url_helper
from . import helper

url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/issues/1347'
)

label_url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/labels/bug'
)

get_issue_example_data = create_example_data_helper(
    'issue_example'
)

get_issue_label_example_data = create_example_data_helper(
    'issue_label_example'
)


class TestIssue(helper.UnitHelper):

    """Test Issue methods that make simple requests."""

    described_class = github3.issues.Issue
    example_data = get_issue_example_data()

    def test_pull_request(self):
        """Verify the request to retrieve an associated Pull Request."""
        self.instance.pull_request()

        self.session.get.assert_called_once_with(
            self.instance.pull_request_urls['url']
        )

    def test_pull_request_without_urls(self):
        """Verify no request is made if no pull request url is present."""
        self.instance.pull_request_urls = {}
        self.instance.pull_request()

        assert self.session.get.called is False


class TestIssueIterators(helper.UnitIteratorHelper):

    """Test Issue methods that return iterators."""

    described_class = github3.issues.Issue
    example_data = get_issue_example_data()

    def test_comments(self):
        """Test the request to retrieve an issue's comments."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )

    def test_events(self):
        """Test the request to retrieve an issue's events."""
        i = self.instance.events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_labels(self):
        """Test the request to retrieve an issue's labels."""
        i = self.instance.labels()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('labels'),
            params={'per_page': 100},
            headers={}
        )


class TestLabelRequiresAuth(UnitHelper):

    """Test that ensure certain methods on Label class requires auth."""

    described_class = github3.issues.label.Label
    example_data = get_issue_label_example_data()

    def after_setup(self):
        """Disable authention on sessions."""
        self.session.has_auth.return_value = False

    def test_delete(self):
        """Test that deleting a label requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.delete()

    def test_update(self):
        """Test that updating label requires authentication."""
        data = {
            'name': 'newname',
            'color': 'afafaf'
        }

        with pytest.raises(github3.AuthenticationFailed):
            self.instance.update(**data)


class TestLabel(UnitHelper):
    """Unit Test for Label."""

    described_class = github3.issues.label.Label
    example_data = get_issue_label_example_data()

    def test_equality(self):
        """Show that two instances of Label are equal."""
        label = Label(get_issue_label_example_data())
        assert self.instance == label

        label._uniq = ('https://https//api.github.com/repos/sigmavirus24/'
                       'github3.py/labels/wontfix')

        assert self.instance != label

    def test_repr(self):
        """Show that instance string is formatted correctly."""
        assert repr(self.instance) == '<Label [{0}]>'.format(
            self.instance.name)

    def test_str(self):
        """Show that instance is formated as a string correctly."""
        assert str(self.instance) == self.instance.name

    def test_delete(self):
        """Test the request for deleting a label."""
        self.instance.delete()
        assert self.session.delete.called

    def test_update(self):
        """Test the request for updating a label."""
        data = {
            'name': 'newname',
            'color': 'afafaf'
        }

        self.instance.update(**data)
        try:
            self.session.patch.assert_called_once_with(
                label_url_for(),
                data='{"name": "newname", "color": "afafaf"}'
            )
        except AssertionError:
            self.session.patch.assert_called_once_with(
                label_url_for(),
                data='{"color": "afafaf", "name": "newname"}'
            )
