from .base import BaseTest, expect, str_test
from github3.events import Event, _payload_handlers
from github3.orgs import Organization
from github3.repos import RepoComment, Download, Repository
from github3.users import User
from github3.gists import Gist
from github3.issues import Issue, IssueComment
from github3.pulls import PullRequest, ReviewComment
from github3.orgs import Team


class TestEvent(BaseTest):
    def __test_events(self, events):
        expect(events) != []
        for e in events:
            self.assertAreNotNone(e, 'actor', 'created_at', 'id', 'repo',
                    'type')
            if e.org:
                expect(e.org).isinstance(Organization)

            payload = (dict, str_test[0], str_test[1])
            expect(e.payload).isinstance(payload)
            expect(e.is_public()).isinstance(bool)
            expect(e.to_json()).isinstance(dict)
            expect(e.repo).isinstance(tuple)
            expect(repr(e)).is_not_None()

    def test_events(self):
        expect(Event.list_types()) != []

        events = self.g.list_events()
        self.__test_events(events)

        if self.auth:
            user = self._g.user()
            for public in (True, False):
                events = user.list_events(public)
                self.__test_events(events)


def handler(name):
    return _payload_handlers[name]


class TestPayloadHandlers(BaseTest):
    empty_user = {
            'login': '',
            'id': '',
            'avatar_url': '',
            'gravatar_id': '',
            'url': ''
            }
    date_str = '2011-01-26T20:00:00Z'
    empty_repo = {
            'owner': empty_user,
            'created_at': date_str,
            'updated_at': date_str,
            }
    empty_gist = {
            'user': empty_user,
            'files': {
                'test.txt': {
                    'size': '',
                    'filename': 'test.txt',
                    'raw_url': '',
                    'content': 'foo'
                    }
                },
            'created_at': date_str,
            }
    comment = {
            'created_at': date_str,
            'updated_at': date_str,
            'user': empty_user,
            'html_url': 'https://github.com/foo/bar/issues/1',
            }
    issue = {
            'user': empty_user,
            'created_at': date_str,
            'updated_at': date_str,
            'pull_request': {
                'html_url': '',
                'diff_url': '',
                'updated_at': ''
                },
            'labels': [],
            'html_url': 'https://github.com/foo/bar/issues/1',
            }
    link_dir = {'href': ''}

    def test_commitcomment(self):
        h = handler('CommitCommentEvent')
        p = {'comment': self.comment.copy()}
        p['comment'].update({
                'commit_id': '',
                'line': '',
                'path': '',
                'pos': '',
            })
        p = h(p)
        expect(p['comment']).isinstance(RepoComment)

    def test_download(self):
        h = handler('DownloadEvent')
        p = h({
            'download': {
                'url': '',
                'html_url': '',
                'id': '',
                'name': '',
                'description': '',
                'size': '',
                'download_count': 0,
                'content_type': ''
                }
            })
        expect(p['download']).isinstance(Download)

    def test_follow(self):
        h = handler('FollowEvent')
        p = h({'target': self.empty_user})
        expect(p['target']).isinstance(User)

    def test_forkev(self):
        h = handler('ForkEvent')
        p = h({'forkee': self.empty_repo})
        expect(p['forkee']).isinstance(Repository)

    def test_gist(self):
        h = handler('GistEvent')
        p = h({'gist': self.empty_gist})
        expect(p['gist']).isinstance(Gist)

    def test_issuecomment(self):
        h = handler('IssueCommentEvent')
        p = {'issue': self.issue, 'comment': self.comment.copy()}
        p = h(p)
        expect(p['issue']).isinstance(Issue)
        expect(p['comment']).isinstance(IssueComment)

    def test_issueevent(self):
        h = handler('IssuesEvent')
        p = h({'issue': self.issue})
        expect(p['issue']).isinstance(Issue)

    def test_member(self):
        h = handler('MemberEvent')
        p = h({'member': self.empty_user})
        expect(p['member']).isinstance(User)

    def test_pullreqev(self):
        h = handler('PullRequestEvent')
        p = h({
            'pull_request': {
                'created_at': self.date_str,
                'updated_at': self.date_str,
                'merged_at': self.date_str,
                'closed_at': self.date_str,
                'head': {
                    'user': self.empty_user,
                    'repo': self.empty_repo,
                    },
                'base': {
                    'user': self.empty_user,
                    'repo': self.empty_repo,
                    },
                'user': self.empty_user,
                '_links': {
                    'self': self.link_dir,
                    'html': self.link_dir,
                    'comments': self.link_dir,
                    'review_comments': self.link_dir,
                    },
                'url': '',
                }
            })
        expect(p['pull_request']).isinstance(PullRequest)

    def test_pullreqcomm(self):
        h = handler('PullRequestReviewCommentEvent')
        p = {'comment': self.comment.copy()}
        p['comment'].update({
            '_links': {
                'self': self.link_dir,
                'html': self.link_dir,
                'pull_request': self.link_dir
                }
            })
        p = h(p)
        expect(p['comment']).isinstance(ReviewComment)

    def test_team(self):
        h = handler('TeamAddEvent')
        p = h({
            'user': self.empty_user,
            'repo': self.empty_repo,
            'team': {
                'url': '',
                'name': '',
                'id': ''
                }
            })
        expect(p['user']).isinstance(User)
        expect(p['repo']).isinstance(Repository)
        expect(p['team']).isinstance(Team)
