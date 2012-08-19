import base
import github3
from expecter import expect
from github3.users import User
from github3.issues import Issue, IssueComment, IssueEvent, Milestone


class TestIssues(base.BaseTest):
    def test_issue(self):
        issue = self.g.issue(self.sigm, self.todo, '21')
        with expect.raises(github3.GitHubError):
            issue.close()
            issue.add_labels('foo', 'bar')

        expect(issue).isinstance(Issue)

        for ev in issue.list_events():
            expect(ev).isinstance(IssueEvent)

        if issue.milestone:
            expect(issue.milestone).isinstance(Milestone)

        if issue.assignee:
            expect(issue.assignee).isinstance(User)

        for com in issue.list_comments():
            expect(com).isinstance(IssueComment)

        expect(issue.number) > 0
