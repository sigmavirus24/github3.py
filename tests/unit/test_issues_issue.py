"""Unit tests for the Issue class."""
import github3
import pytest
import mock

from github3.issues.label import Label
from github3.issues import Issue
from . import helper

comment_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/issues/comments'
)

url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/issues/1347'
)

label_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/labels/bug'
)

get_issue_example_data = helper.create_example_data_helper(
    'issue_example'
)

get_issue_event_example_data = helper.create_example_data_helper(
    'issue_event_example'
)
get_issue_label_example_data = helper.create_example_data_helper(
    'issue_label_example'
)


class TestIssueRequiresAuth(helper.UnitHelper):

    """Test Issue methods that require Authentication."""

    described_class = github3.issues.Issue
    example_data = get_issue_example_data()

    def after_setup(self):
        self.session.has_auth.return_value = False

    def test_add_labels(self):
        """Verify that adding a label requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.add_labels('enhancement')

    def test_assign(self):
        """Verify that assigning an issue requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.assign('sigmavirus24')

    def test_close(self):
        """Verify that closing an issue requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.close()

    def test_create_comment(self):
        """Verify that creating a comment requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.create_comment(body='comment body')

    def test_edit_comment(self):
        """Verify that editing a comment requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.edit()

    def test_remove_all_labels(self):
        """Verify that removing all labels requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.remove_all_labels()

    def test_remove_label(self):
        """Verify that removing a label requires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.remove_label('enhancement')

    def test_reopen(self):
        """Verify that reopening an issue equires authentication."""
        with pytest.raises(github3.AuthenticationFailed):
            self.instance.reopen()


class TestIssue(helper.UnitHelper):

    """Test Issue methods that make simple requests."""

    described_class = github3.issues.Issue
    example_data = get_issue_example_data()

    def test_add_labels(self):
        """Verify the request for adding a label."""
        self.instance.add_labels('enhancement')
        self.post_called_with(
            url_for('labels'),
            data=['enhancement']
        )

    def test_assign(self):
        """Verify the request for assigning an issue."""
        with mock.patch.object(Issue, 'edit') as edit:
            edit.return_value = True
            labels = [str(label) for label in self.instance.original_labels]
            self.instance.assign(username='sigmavirus24')
            edit.assert_called_once_with(
                self.instance.title,
                self.instance.body,
                'sigmavirus24',
                self.instance.state,
                self.instance.milestone.number,
                labels
            )

    def test_assign_empty_username(self):
        """Verify the request when assigning a username."""
        self.instance.assign('')
        assert self.session.patch.called is False

    def test_close(self):
        """Verify the request for closing an issue."""
        self.instance.close()
        labels = [str(label) for label in self.instance.original_labels]
        self.patch_called_with(
            url_for(),
            data={
                'assignee': self.instance.assignee.login or '',
                'body': self.instance.body,
                'labels': labels,
                'milestone': self.instance.milestone.number or '',
                'state': 'closed',
                'title': self.instance.title
            }
        )

    def test_comment(self):
        """Verify the request for retrieving an issue comment."""
        self.instance.comment(1)
        self.session.get.assert_called_once_with(
            comment_url_for('1')
        )

    def test_create_comment(self):
        """Verify the request for creating a comment."""
        data = {
            'body': 'comment body'
        }
        self.instance.create_comment(**data)
        self.post_called_with(
            url_for('comments'),
            data=data
        )

    def test_create_comment_required_body(self):
        """Verify request is not made when comment body is empty."""
        self.instance.create_comment(body='')
        assert self.session.post.called is False

    def test_comment_positive_id(self):
        """Verify the request for retrieving an issue comment."""
        self.instance.comment(-1)
        assert self.session.get.called is False

    def test_edit(self):
        """Verify the request for editing an issue."""
        data = {
            'title': 'issue title',
            'body': 'issue body',
            'assignee': 'sigmavirus24',
            'state': 'closed',
            'labels': []
        }
        self.instance.edit(**data)
        self.patch_called_with(
            url_for(),
            data=data
        )

    def test_edit_milestone(self):
        """Verify the request for editing an issue."""
        data = {
            'title': 'issue title',
            'body': 'issue body',
            'assignee': 'sigmavirus24',
            'state': 'closed',
            'labels': [],
            'milestone': 0
        }

        self.instance.edit(**data)
        data['milestone'] = None
        self.patch_called_with(
            url_for(),
            data=data
        )

    def test_edit_no_parameters(self):
        """Verify request is not made editing an issue with no parameters."""
        self.instance.edit()
        assert self.session.patch.called is False

    def test_enterprise(self):
        """Show that enterprise data can be instantiated as Issue."""
        json = helper.create_example_data_helper('issue_enterprise')()
        assert github3.issues.Issue(json)

    def test_equality(self):
        """Show that two instances of Issue are equal."""
        issue = github3.issues.Issue(get_issue_example_data())
        assert self.instance == issue

        issue._uniq = 1
        assert self.instance != issue

    def test_is_closed(self):
        """Test an issue is closed."""
        assert self.instance.is_closed() is False

        self.instance.state = 'closed'
        assert self.instance.is_closed() is True

    def test_issue_137(self):
        """
        GitHub sometimes returns `pull` as part of of the `html_url` for Issue
        requests.
        """
        issue = Issue(helper.create_example_data_helper('issue_137')())
        self.assertEqual(
            issue.html_url,
            "https://github.com/sigmavirus24/github3.py/pull/1")
        self.assertEqual(issue.repository, ("sigmavirus24", "github3.py"))

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

    def test_repr(self):
        """Show that instance string is formattted properly."""
        assert repr(self.instance) == '<Issue [{r[0]}/{r[1]} #{n}]>'.format(
            r=self.instance.repository,
            n=self.instance.number
        )

    def test_remove_all_labels(self):
        """Verify that all labels are removed."""
        with mock.patch.object(Issue, 'replace_labels') as replace_labels:
            replace_labels.return_value = []
            assert self.instance.remove_all_labels() == []
            replace_labels.assert_called_once_with([])

    def test_remove_label(self):
        """Verify the request for removing a label from an issue."""
        self.instance.remove_label('enhancement')

        self.session.delete.assert_called_once_with(
            url_for('labels/enhancement')
        )

    def test_reopen(self):
        """Test the request for reopening an issue."""
        labels = [str(label) for label in self.instance.original_labels]
        with mock.patch.object(Issue, 'edit') as edit:
            self.instance.reopen()
            edit.assert_called_once_with(
                self.instance.title,
                self.instance.body,
                self.instance.assignee.login,
                'open',
                self.instance.milestone.number,
                labels
            )

    def test_replace_labels(self):
        """Verify the request for replacing labels."""
        labels = ['foo', 'bar']
        self.instance.replace_labels(labels)
        self.put_called_with(
            url_for('labels'),
            data=labels
        )


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


class TestLabelRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Test that ensure certain methods on Label class requires auth."""

    described_class = github3.issues.label.Label
    example_data = get_issue_label_example_data()

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


class TestLabel(helper.UnitHelper):
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
        self.patch_called_with(
            label_url_for(),
            data=data
        )


class TestIssueEvent(helper.UnitHelper):

    """Unit test for IssueEvent."""

    described_class = github3.issues.event.IssueEvent
    example_data = get_issue_event_example_data()

    def test_repr(self):
        """Show that instance string is formatted correctly."""
        assert repr(self.instance) == '<Issue Event [{0} by {1}]>'.format(
            'closed', 'octocat'
        )

    def test_equality(self):
        """Show that two instances of IssueEvent are equal."""
        issue_event = github3.issues.event.IssueEvent(
            get_issue_event_example_data()
        )

        assert self.instance == issue_event
        issue_event._uniq = 'foo'
        assert self.instance != issue_event
