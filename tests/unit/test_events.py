import github3
from unittest import TestCase
from .helper import UnitHelper
from .helper import create_example_data_helper

get_example_data = create_example_data_helper('event_example')
get_org_example_data = create_example_data_helper('org_example')
get_comment_example_data = create_example_data_helper('comment_example')
get_pull_request_example_data = create_example_data_helper(
    'pull_request_example'
)
get_issue_example_data = create_example_data_helper('issue_example')
get_user_example_data = create_example_data_helper('user_example')
get_repo_example_data = create_example_data_helper('repo_example')
get_gist_example_data = create_example_data_helper('gist_example')
get_team_example_data = create_example_data_helper('team_example')


class TestEvent(UnitHelper):

    described_class = github3.events.Event
    example_data = get_example_data()

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert repr(self.instance).startswith('<Event')

    def test_list_types(self):
        """Show that an event contains sorted payload handlers."""
        Event, handlers = (github3.events.Event,
                           github3.events._payload_handlers)

        assert Event.list_types() == sorted(handlers.keys())

    def test_org(self):
        """Show that an event contains an organization instance."""
        json = self.instance.as_dict().copy()
        org = get_org_example_data()
        json['org'] = org
        event = github3.events.Event(json)
        assert isinstance(event.org, github3.orgs.Organization)


class TestPayLoadHandlers(TestCase):

    def test_commitcomment(self):
        """Show that the event type is a RepoComment."""
        comment = {'comment': get_comment_example_data()}
        comment = github3.events._commitcomment(comment, None)
        assert isinstance(comment['comment'],
                          github3.repos.comment.RepoComment)

    def test_follow(self):
        """Show that the event type is a FollowEvent."""
        follower = {'target': get_user_example_data()}
        github3.events._follow(follower, None)
        assert isinstance(follower['target'], github3.events.EventUser)

    def test_forkev(self):
        """Show that the event type is a ForkEvent."""
        forkee = {'forkee': get_repo_example_data()}
        github3.events._forkev(forkee, None)
        assert isinstance(forkee['forkee'], github3.repos.Repository)

    def test_gist(self):
        """Show that the event type is a GistEvent."""
        gist = {'gist': get_gist_example_data()}
        github3.events._gist(gist, None)
        assert isinstance(gist['gist'], github3.gists.Gist)

    def test_issuecomm(self):
        """Show that the event type is a IssueCommentEvent."""
        comment = {
            'issue': get_issue_example_data(),
            'comment': get_comment_example_data()
        }
        github3.events._issuecomm(comment, None)
        assert isinstance(comment['issue'], github3.issues.Issue)
        assert isinstance(comment['comment'],
                          github3.issues.comment.IssueComment)

    def test_issueevent(self):
        """Show that the event type is a IssueEvent."""
        comment = {'issue': get_issue_example_data()}
        github3.events._issueevent(comment, None)
        assert isinstance(comment['issue'], github3.issues.Issue)

    def test_member(self):
        """Show that the event type is a MemberEvent."""
        member = {'member': get_user_example_data()}
        github3.events._member(member, None)
        assert isinstance(member['member'], github3.events.EventUser)

    def test_pullreqev(self):
        """Show that the event type is a PullRequestEvent."""
        pull_request = {'pull_request': get_pull_request_example_data()}
        github3.events._pullreqev(pull_request, None)
        assert isinstance(pull_request['pull_request'],
                          github3.pulls.PullRequest)

    def test_pullreqcomment(self):
        """Show that the event type is a PullRequestReviewCommentEvent."""
        pull_request = {'comment': get_comment_example_data()}
        github3.events._pullreqcomm(pull_request, None)
        assert isinstance(pull_request['comment'], github3.pulls.ReviewComment)

    def test_team(self):
        """Show that the event type is a TeamAddEvent."""
        team = {
            'team': get_team_example_data(),
            'repo': get_repo_example_data(),
            'user': get_user_example_data()
        }

        github3.events._team(team, None)
        assert isinstance(team['team'], github3.orgs.Team)
        assert isinstance(team['repo'], github3.repos.Repository)
