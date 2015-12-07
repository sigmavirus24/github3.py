"""Unit tests for the Milestone class."""
import github3

from .helper import UnitIteratorHelper, create_url_helper,create_example_data_helper

get_milestone_example_data = create_example_data_helper('milestone_example')
example_data = get_milestone_example_data()

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
