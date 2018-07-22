"""Unit tests for the Milestone class."""
import datetime
import github3

from . import helper

get_milestone_example_data = helper.create_example_data_helper(
    'milestone_example'
)
example_data = get_milestone_example_data()

url_for = helper.create_url_helper("https://api.github.com/repos/octocat/"
                                   "Hello-World/milestones/1")


class TestMilestoneRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    """Test Milestone methods that require authentication."""

    described_class = github3.issues.milestone.Milestone
    example_data = example_data

    def test_delete(self):
        """Test that deleting milestone requires authentication."""
        self.assert_requires_auth(self.instance.delete)

    def test_update(self):
        """Test that updating a milestone requires authentication."""
        data = {
            'title': 'foo',
            'state': 'closed',
            'description': ':sparkles:',
            'due_on': '2013-12-31T23:59:59Z'
        }
        self.assert_requires_auth(self.instance.update, **data)


class TestMilestone(helper.UnitHelper):
    """Test Milestone methods."""

    described_class = github3.issues.milestone.Milestone
    example_data = example_data

    def test_delete(self):
        """Test the request for deleting a milestone."""
        self.instance.delete()

        assert self.session.delete.called

    def test_none_creator(self):
        """Show that creator is None when json attribute is set to None."""
        json = self.instance.as_dict().copy()
        json['creator'] = None
        milestone = github3.issues.milestone.Milestone(json, self.session)
        assert milestone.creator is None

    def test_due_on(self):
        """Show that due on attribute is a datetime object."""
        json = self.instance.as_dict().copy()
        json['due_on'] = '2012-12-31T23:59:59Z'
        milestone = github3.issues.milestone.Milestone(json, self.session)
        assert isinstance(milestone.due_on, datetime.datetime)

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert repr(self.instance) == '<Milestone [v1.0]>'

    def test_str(self):
        """Show that str(milestone) is the same as milestone's title."""
        assert str(self.instance) == 'v1.0'

    def test_id(self):
        """Show that id of instance is returned correctly."""
        assert self.instance.id == 1002604

    def test_update(self):
        """Test the request for updating a milestone."""
        data = {
            'title': 'foo',
            'state': 'closed',
            'description': ':sparkles:',
            'due_on': '2013-12-31T23:59:59Z'
        }
        self.instance.update(**data)
        self.patch_called_with(
            url_for(),
            data=data
        )

    def test_update_no_parameters(self):
        """Show request is not made when update is called with no arguments."""
        self.instance.update()

        assert self.session.post.called is False


class TestMilestoneIterator(helper.UnitIteratorHelper):

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
