"""Unit tests for the Milestone class."""
import github3

from .helper import (UnitIteratorHelper, create_url_helper,)

example_data = {
    "url": "https://api.github.com/repos/octocat/Hello-World/milestones/1",
    "number": 1,
    "state": "open",
    "title": "v1.0",
    "description": "",
    "creator": {
        "login": "octocat",
        "id": 1,
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "somehexcode",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": ("https://api.github.com/users/octocat/following"
                          "{/other_user}"),
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": ("https://api.github.com/users/octocat/starred"
                        "{/owner}{/repo}"),
        "subscriptions_url": ("https://api.github.com/users/octocat/"
                              "subscriptions"),
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": ("https://api.github.com/users/octocat/"
                                "received_events"),
        "type": "User",
        "site_admin": False
    },
    "open_issues": 4,
    "closed_issues": 8,
    "created_at": "2011-04-10T20:09:31Z",
    "updated_at": "2014-03-03T18:58:10Z",
    "due_on": None
}

url_for = create_url_helper("https://api.github.com/repos/octocat/Hello-World/"
                            "milestones/1")


class TestMilestoneIterator(UnitIteratorHelper):

    """Test Milestone methods that return iterators."""

    described_class = github3.issues.milestone.Milestone
    example_data = example_data

    def test_labels(self):
        """Test the request to retrieve labels associated with a milestone."""
        i = self.instance.labels()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('labels'),
            params={'per_page': 100},
            headers={}
        )
