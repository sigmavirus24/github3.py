import github3
from base import BaseTest, expect, str_test
from datetime import datetime
from github3.users import User
from github3.issues import Issue, IssueComment, IssueEvent, Label, Milestone


class TestIssue(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssue, self).__init__(methodName)
        self.issue = self.g.issue(self.kr, 'requests', 2)

    def test_issue(self):
        expect(self.issue).isinstance(Issue)

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.issue.close()
            self.issue.add_labels('foo', 'bar')
            self.issue.edit('Foo', 'Bar', self.sigm, 'closed')
            self.issue.remove_label('Bug')
            self.issue.remove_all_labels()
            self.issue.repoen()

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
        expect(self.issue.comment(2965299)).isinstance(IssueComment)

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

    def test_with_auth(self):
        if not self.auth:
            return

        issue = self._g.issue(self.gh3py, self.test_repo, '1')

        # I would like to try this functionality but right now, I
        # (sigmavirus24) am the only person with permission on the org and
        # I am the issue creator so for others it may not work and that is
        # not a failure, just standard Github behavior
        try:
            issue.close()
            issue.reopen()
            old_title = issue.title
            old_body = issue.body
            issue.edit('New title', 'Monty spam spam python spam')
            issue.edit(old_title, old_body)
        except github3.GitHubError:
            pass


class TestLabel(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestLabel, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '6')
        self.label = issue.labels[0]

    def test_label(self):
        expect(self.label).isinstance(Label)

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.label.delete()
            self.label.update('foo', 'abc123')

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
        expect(label.delete()).is_True()


class TestMilestone(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestMilestone, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '179')
        self.milestone = issue.milestone

    def test_milestone(self):
        expect(self.milestone).isinstance(Milestone)

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.milestone.delete()
            self.milestone.update('New title', 'closed')

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
        m.update('test_update', 'closed')
        expect(m.delete()).is_True()


class TestIssueComment(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestIssueComment, self).__init__(methodName)
        issue = self.g.issue(self.kr, 'requests', '179')
        self.comment = issue.list_comments()[0]

    def test_comment(self):
        expect(self.comment).isinstance(IssueComment)

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
        with expect.raises(github3.GitHubError):
            self.comment.delete()
            self.comment.edit('foo')

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
        issue = self.g.issue(self.kr, 'requests', 179)
        self.ev = issue.list_events()[0]

    def test_issueevent(self):
        expect(self.ev).isinstance(IssueEvent)

    def test_event(self):
        expect(self.ev.event).isinstance(str_test)

    def test_commit_id(self):
        if self.ev.commit_id:
            expect(self.ev.commit_id).isinstance(str_test)

    def test_created_at(self):
        expect(self.ev.created_at).isinstance(datetime)

    def test_issue(self):
        expect(self.ev.issue).isinstance(Issue)

    def test_comments(self):
        expect(self.ev.comments) >= 0

    def test_pull_request(self):
        expect(self.ev.pull_request).isinstance(dict)

    def test_updated_at(self):
        if self.ev.updated_at:
            expect(self.ev.updated_at).isinstance(datetime)
