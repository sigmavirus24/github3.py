"""Unit tests for Deployment methods."""
import github3

from .helper import (UnitIteratorHelper, create_url_helper,
                     create_example_data_helper)

url_for = create_url_helper(
    'https://api.github.com/repos/octocat/example/deployments/1'
)

get_repo_example_data = create_example_data_helper('repos_deployment_example')

example_data = get_repo_example_data()


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
