"""Unit tests for Deployment methods."""
import github3

from .helper import UnitIteratorHelper, create_url_helper

url_for = create_url_helper(
    'https://api.github.com/repos/octocat/example/deployments/1'
)

example_data = {
    "url": "https://api.github.com/repos/octocat/example/deployments/1",
    "id": 1,
    "sha": "a84d88e7554fc1fa21bcbc4efae3c782a70d2b9d",
    "ref": "master",
    "task": "deploy",
    "payload": {
        "task": "deploy:migrate"
    },
    "environment": "production",
    "description": "Deploy request from hubot",
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
    "created_at": "2012-07-20T01:19:13Z",
    "updated_at": "2012-07-20T01:19:13Z",
    "statuses_url": ("https://api.github.com/repos/octocat/example/"
                     "deployments/1/statuses"),
    "repository_url": "https://api.github.com/repos/octocat/example"
}


class TestDeploymentIterators(UnitIteratorHelper):

    """Test Deployment methods that return iterators."""

    described_class = github3.repos.deployment.Deployment
    example_data = example_data

    def test_statuses(self):
        """Test the request to retrieve a deployment's statuses."""
        i = self.instance.statuses()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('statuses'),
            params={'per_page': 100},
            headers={}
        )
