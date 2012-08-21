import base
import github3
from expecter import expect
from datetime import datetime
from github3.users import User
from github3.issues import Issue, IssueComment, IssueEvent, Label, Milestone


class TestIssues(base.BaseTest):
    def test_issue(self):
        issue = self.g.issue(self.sigm, self.todo, '2')
        with expect.raises(github3.GitHubError):
            issue.close()
            issue.add_labels('foo', 'bar')
            issue.edit('Foo', 'Bar', self.sigm, 'closed')
            issue.remove_label('Bug')
            issue.remove_all_labels()
            issue.repoen()

        expect(issue).isinstance(Issue)

        if issue.assignee:
            expect(issue.assignee).isinstance(User)

        expect(issue.body).isinstance(base.str_test)
        expect(issue.created_at).isinstance(datetime)
        expect(issue.closed_at).isinstance(datetime)
        expect(issue.comment(2965299)).isinstance(IssueComment)
        expect(issue.html_url).isinstance(base.str_test)
        expect(issue.id) > 0
        expect(issue.is_closed()).isinstance(bool)

        for label in issue.labels:
            expect(label).isinstance(Label)

        for ev in issue.list_events():
            expect(ev).isinstance(IssueEvent)

        if issue.milestone:
            expect(issue.milestone).isinstance(Milestone)

        for com in issue.list_comments():
            expect(com).isinstance(IssueComment)

        expect(issue.number) > 0
        expect(issue.pull_request).isinstance(dict)
        expect(issue.repository).isinstance(tuple)
        expect(issue.state).isinstance(base.str_test)

        if issue.state not in ('open', 'closed'):
            self.fail('State not valid')

        if issue.title:
            expect(issue.title).isinstance(base.str_test)

        expect(issue.updated_at).isinstance(datetime)
        expect(issue.user).isinstance(User)

        if self.auth:
            issue = self._g.issue(self.gh3py, self.test_repo, '1')
            c = issue.create_comment('Test commenting')
            expect(c).isinstance(IssueComment)
            expect(c.delete()).is_True()

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

    def test_label(self):
        issue = self.g.issue(self.sigm, self.todo, '6')
        label = issue.labels[0]

        expect(label).isinstance(Label)

        with expect.raises(github3.GitHubError):
            label.delete()
            label.update('foo', 'abc123')

        expect(label.name) == 'Enhancement'
        expect(label.color) != ''

    def test_milestone(self):
        issue = self.g.issue(self.sigm, self.todo, '6')
        milestone = issue.milestone

        with expect.raises(github3.GitHubError):
            milestone.delete()
            milestone.update('New title', 'closed')

        expect(milestone.closed_issues) == 5
        expect(milestone.created_at).isinstance(datetime)
        expect(milestone.creator).isinstance(User)
        expect(milestone.description) == 'Next stable release'
        if milestone.due_on:
            expect(milestone.due_on).isinstance(datetime)

        for l in milestone.list_labels():
            expect(l).isinstance(Label)

        expect(milestone.number) > 0
        expect(milestone.open_issues) == 0
        expect(milestone.state) == 'closed'
        expect(milestone.title) == '0.2'

    def test_comment(self):
        issue = self.g.issue(self.sigm, self.todo, '2')
        comment = issue.list_comments()[0]
        expect(comment).isinstance(IssueComment)
        expect(comment.updated_at).isinstance(datetime)
        self.assertAreNotNone(comment, 'body', 'body_html', 'body_text',
                'created_at', 'user')
        expect(comment.created_at).isinstance(datetime)
        expect(comment.id) > 0
        expect(comment.user).isinstance(User)
        with expect.raises(github3.GitHubError):
            comment.delete()
            comment.edit('foo')
