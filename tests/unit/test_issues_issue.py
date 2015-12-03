"""Unit tests for the Issue class."""
import github3

from . import helper

url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/issues/1347'
)

get_issue_example_data = helper.create_example_data_helper(
    'issue_example'
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
