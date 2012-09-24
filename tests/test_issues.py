from .base import BaseTest, expect, str_test
from datetime import datetime
from github3.users import User
from github3.issues import (Issue, IssueComment, IssueEvent, Label, Milestone,
        issue_params)


class TestIssue(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssue, self).__init__(methodName)
        self.issue = self.g.issue(self.kr, 'requests', 2)

    def test_issue(self):
        expect(self.issue).isinstance(Issue)
        expect(repr(self.issue)) != ''

    def test_requires_auth(self):
        self.raisesGHE(self.issue.close)
        self.raisesGHE(self.issue.add_labels, 'foo', 'bar')
        self.raisesGHE(self.issue.edit, 'Foo', 'Bar', self.sigm, 'closed')
        self.raisesGHE(self.issue.remove_label, 'Bug')
        self.raisesGHE(self.issue.remove_all_labels)
        self.raisesGHE(self.issue.reopen)

    def test_assignee(self):
        if self.issue.assignee:
            expect(self.issue.assignee).isinstance(User)

    def test_body(self):
        expect(self.issue.body).isinstance(str_test)

    def test_created_at(self):
        expect(self.issue.created_at).isinstance(datetime)

    def test_closed_at(self):
        expect(self.issue.closed_at).isinstance(datetime)

    def test_comment(self):
        expect(self.issue.comment(770775)).isinstance(IssueComment)

    def test_html_url(self):
        expect(self.issue.html_url).isinstance(str_test)

    def test_id(self):
        expect(self.issue.id) > 0

    def test_is_closed(self):
        expect(self.issue.is_closed()).isinstance(bool)

    def test_labels(self):
        self.expect_list_of_class(self.issue.labels, Label)

    def test_list_events(self):
        self.expect_list_of_class(self.issue.list_events(), IssueEvent)

    def test_milestone(self):
        if self.issue.milestone:
            expect(self.issue.milestone).isinstance(Milestone)

    def test_list_comments(self):
        self.expect_list_of_class(self.issue.list_comments(), IssueComment)

    def test_number(self):
        expect(self.issue.number) > 0

    def test_pull_request(self):
        expect(self.issue.pull_request).isinstance(dict)

    def test_repository(self):
        expect(self.issue.repository).isinstance(tuple)

    def test_state(self):
        expect(self.issue.state).isinstance(str_test)
        if self.issue.state not in ('open', 'closed'):
            self.fail('State not valid')

    def test_title(self):
        if self.issue.title:
            expect(self.issue.title).isinstance(str_test)

    def test_updated_at(self):
        expect(self.issue.updated_at).isinstance(datetime)

    def test_user(self):
        expect(self.issue.user).isinstance(User)

    def test_issue_params(self):
        faulty_params = {'filter': 'foo', 'sort': 'sorted', 'direction': 'up',
                'since': 'yesterday', 'state': 'clopen', 'labels': ''}
        # clopen is a real word in mathematics, check it out
        expect(issue_params(**faulty_params)) == {}
        good_params = {'filter': 'assigned', 'sort': 'created',
                'direction': 'asc', 'since': '2012-01-20T20:00:00Z',
                'state': 'open', 'labels': 'Enhancement,bug'}
        expect(issue_params(**good_params)) == good_params

    def test_with_auth(self):
        if not self.auth:
            return

        issue = self._g.issue(self.gh3py, self.test_repo, '1')

        # I would like to try this functionality but right now, I
        # (sigmavirus24) am the only person with permission on the org and
        # I am the issue creator so for others it may not work and that is
        # not a failure, just standard Github behavior
        issue.close()
        issue.reopen()
        expect(issue.is_closed()).is_False()
        old_title = issue.title
        old_body = issue.body
        issue.edit('New title', 'Monty spam spam python spam')
        issue.edit(old_title, old_body)
        expect(issue.edit(None)).is_False()
        issue.add_labels('wontfix', 'Enhancement')
        expect(issue.remove_label('wontfix')).isinstance(list)
        expect(issue.remove_label('wontfix')).isinstance(list)
        expect(issue.replace_labels(['invalid', 'duplicate'])).is_True()
        expect(issue.remove_all_labels()).is_True()


class TestLabel(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestLabel, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '6')
        self.label = issue.labels[0]

    def test_label(self):
        expect(self.label).isinstance(Label)
        expect(repr(self.label)) != ''

    def test_requires_auth(self):
        self.raisesGHE(self.label.delete)
        self.raisesGHE(self.label.update, 'foo', 'abc123')

    def test_name(self):
        expect(self.label.name) == 'Feature Request'

    def test_color(self):
        expect(self.label.color) != ''

    def test_with_auth(self):
        if not self.auth:
            return

        repo = self._g.repository(self.gh3py, self.test_repo)
        label = repo.create_label('Test_label', 'abc123')
        expect(label.color) == 'abc123'
        expect(label.name) == 'Test_label'
        expect(label.update('Test_update', 'abd124')).is_True()
        expect(label.update('Test_update2', '#abd124')).is_True()
        expect(label.update(None, None)).is_False()
        expect(label.delete()).is_True()


class TestMilestone(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestMilestone, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '179')
        self.milestone = issue.milestone

    def test_milestone(self):
        expect(self.milestone).isinstance(Milestone)
        expect(repr(self.milestone)) != ''

    def test_requires_auth(self):
        self.raisesGHE(self.milestone.delete)
        self.raisesGHE(self.milestone.update, 'New title', 'closed')

    def test_closed_issues(self):
        expect(self.milestone.closed_issues) >= 6

    def test_created_at(self):
        expect(self.milestone.created_at).isinstance(datetime)

    def test_creator(self):
        expect(self.milestone.creator).isinstance(User)

    def test_description(self):
        expect(self.milestone.description) == 'Way out there.'

    def test_due_on(self):
        if self.milestone.due_on:
            expect(self.milestone.due_on).isinstance(datetime)

    def test_list_labels(self):
        self.expect_list_of_class(self.milestone.list_labels(), Label)

    def test_number(self):
        expect(self.milestone.number) > 0

    def test_open_issues(self):
        expect(self.milestone.open_issues) >= 0

    def test_state(self):
        expect(self.milestone.state in ('closed', 'open')).is_True()

    def test_title(self):
        expect(self.milestone.title) == 'v1.0.0'

    def test_with_auth(self):
        if not self.auth:
            return

        repo = self._g.repository(self.gh3py, self.test_repo)
        m = repo.create_milestone('test_creation', 'open')
        expect(m).isinstance(Milestone)
        expect(m.update('test_update', 'closed')).is_True()
        expect(m.update(None)).is_False()
        expect(m.delete()).is_True()
        m = None
        m = repo.create_milestone('test_creation')
        expect(m).isinstance(Milestone)
        expect(m.delete()).is_True()


class TestIssueComment(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssueComment, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '179')
        self.comment = issue.list_comments()[0]

    def test_comment(self):
        expect(self.comment).isinstance(IssueComment)
        expect(repr(self.comment)) != ''

    def test_created_at(self):
        expect(self.comment.created_at).isinstance(datetime)

    def test_updated_at(self):
        expect(self.comment.updated_at).isinstance(datetime)

    def test_body(self):
        expect(self.comment.body).isinstance(str_test)

    def test_body_html(self):
        expect(self.comment.body_html).isinstance(str_test)

    def test_body_text(self):
        expect(self.comment.body_text).isinstance(str_test)

    def test_id(self):
        expect(self.comment.id) > 0

    def test_user(self):
        expect(self.comment.user).isinstance(User)

    def test_requires_auth(self):
        self.raisesGHE(self.comment.delete)
        self.raisesGHE(self.comment.edit, 'foo')

    def test_with_auth(self):
        if not self.auth:
            return

        issue = self._g.issue(self.gh3py, self.test_repo, '1')
        c = issue.create_comment('Test commenting')
        expect(c).isinstance(IssueComment)
        expect(c.edit('Test editing comments')).is_True()
        expect(c.delete()).is_True()


class TestIssueEvent(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssueEvent, self).__init__(methodName)
        repo = self.g.repository(self.kr, 'requests')
        issue = repo.issue(179)
        self.ev = issue.list_events()[0]
        self.repo_ev = repo.list_issue_events()[0]

    def test_issueevent(self):
        expect(self.ev).isinstance(IssueEvent)
        expect(repr(self.ev)) != ''

    def test_event(self):
        expect(self.ev.event).isinstance(str_test)

    def test_commit_id(self):
        if self.ev.commit_id:
            expect(self.ev.commit_id).isinstance(str_test)

    def test_created_at(self):
        expect(self.ev.created_at).isinstance(datetime)

    def test_issue(self):
        expect(self.ev.issue).isinstance(Issue)
        expect(self.repo_ev.issue).isinstance(Issue)

    def test_comments(self):
        expect(self.ev.comments) >= 0

    def test_pull_request(self):
        expect(self.ev.pull_request).isinstance(dict)
