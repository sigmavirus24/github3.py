from .base import BaseTest, expect, str_test
from datetime import datetime
from github3.git import Commit
from github3.pulls import (PullRequest, PullDestination, ReviewComment,
        PullFile)
from github3.users import User


class TestPullRequest(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestPullRequest, self).__init__(methodName)
        repo = self.g.repository(self.kr, 'requests')
        self.pr = repo.pull_request(833)
        self.body = [
        ('Use dicts and lists where necessary but accept both dicts and lists'
            ' of'), '2-tuples everywhere.'
        ]
        self.body_html = [
        ('<p>'
         'Use dicts and lists where necessary but accept both dicts and lists'
         ' of'
         '<br>'),
         '2-tuples everywhere.</p>'
        ]
        self.url = 'https://github.com/{0}/requests/pull/833'.format(self.kr)

    def test_pull_request(self):
        expect(self.pr).isinstance(PullRequest)
        expect(repr(self.pr)) != ''

    def test_base(self):
        expect(self.pr.base).is_not_None()
        expect(self.pr.base).isinstance(PullDestination)
        expect(self.pr.base.label) == 'kennethreitz:develop'

    def test_body(self):
        expect(self.pr.body).isinstance(str_test)
        body = '\n'.join(self.body)
        expect(self.pr.body) == body

    def test_body_html(self):
        expect(self.pr.body_html).isinstance(str_test)
        body = '\n'.join(self.body_html)
        expect(self.pr.body_html) == body

    def test_body_text(self):
        expect(self.pr.body_text).isinstance(str_test)
        body = '\n'.join(self.body)
        expect(self.pr.body_text) == body

    def test_closed_at(self):
        expect(self.pr.closed_at).isinstance(datetime)

    def test_created_at(self):
        expect(self.pr.created_at).isinstance(datetime)

    def test_diff_url(self):
        url = self.pr.diff_url
        expect(url).isinstance(str_test)
        expect(url) == self.url + '.diff'

    def test_head(self):
        head = self.pr.head
        label = head.label
        expect(head).isinstance(PullDestination)
        expect(label) == 'sigmavirus24:fix_key_val_args'

    def test_html_url(self):
        url = self.pr.html_url
        expect(url).isinstance(str_test)
        expect(url) == self.url

    def test_id(self):
        expect(self.pr.id) == 2228458

    def test_is_mergeable(self):
        expect(self.pr.is_mergeable()).is_False()

    def test_is_merged(self):
        expect(self.pr.is_merged()).is_True()

    def test_issue_url(self):
        expect(self.pr.issue_url).isinstance(str_test)
        expect(self.pr.issue_url) == self.url.replace('pull', 'issues')

    def test_links(self):
        expect(self.pr.links).isinstance(dict)
        links = ['comments', 'html', 'issue', 'review_comments', 'self']
        expect(sorted(list(self.pr.links.keys()))) == links

    def test_list_comments(self):
        comments = self.pr.list_comments()
        self.expect_list_of_class(comments, ReviewComment)

    def test_list_commits(self):
        commits = self.pr.list_commits()
        self.expect_list_of_class(commits, Commit)

    def test_list_files(self):
        files = self.pr.list_files()
        self.expect_list_of_class(files, PullFile)

    def test_merged_at(self):
        expect(self.pr.merged_at).isinstance(datetime)

    def test_merged_by(self):
        u = self.pr.merged_by
        expect(u).isinstance(User)
        expect(u.login) == self.kr

    def test_number(self):
        expect(self.pr.number) == 833

    def test_patch_url(self):
        expect(self.pr.patch_url).isinstance(str_test)
        expect(self.pr.patch_url) == self.url + '.patch'

    def test_requires_auth(self):
        self.raisesGHE(self.pr.merge, 'foo bar')
        self.raisesGHE(self.pr.update, 'New title')

    def test_state(self):
        expect(self.pr.state) == 'closed'

    def test_title(self):
        expect(self.pr.title) == 'Fixes #817.'

    def test_user(self):
        expect(self.pr.user).isinstance(User)
        expect(self.pr.user.login) == self.sigm

    def test_with_auth(self):
        if not self.auth:
            return
        r = self._g.repository(self.gh3py, self.test_repo)
        pr = r.pull_request(2)
        title, body, state = pr.title, pr.body, pr.state
        expect(pr.update('Test editing', 'New body')).is_True()
        expect(pr.update(title, body, state)).is_True()
        expect(pr.update()).is_False()


class TestReviewComment(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestReviewComment, self).__init__(methodName)
        repo = self.g.repository(self.kr, 'requests')
        self.comment = repo.pull_request(819).list_comments()[0]

    def test_review_comment(self):
        expect(self.comment).isinstance(ReviewComment)
        expect(repr(self.comment)) != ''

    def test_body(self):
        expect(self.comment.body).isinstance(str_test)

    def test_body_html(self):
        html = self.comment.body_html
        if html:
            expect(html).isinstance(str_test)

    def test_body_text(self):
        text = self.comment.body_text
        if text:
            expect(text).isinstance(str_test)

    def test_created_at(self):
        expect(self.comment.created_at).isinstance(datetime)

    def test_commit_id(self):
        cid = self.comment.commit_id
        expect(cid).isinstance(str_test)
        expect(cid) == 'babac7368b9aa34fd1f0e5d29d4f80c2006ad614'

    def test_html_url(self):
        url = ('https://github.com/kennethreitz/requests'
        '/pull/819#discussion_r1472088')
        expect(self.comment.html_url).isinstance(dict)
        expect(self.comment.html_url['href']) == url

    def test_id(self):
        expect(self.comment.id) == 1472088

    def test_path(self):
        expect(self.comment.path).isinstance(str_test)
        expect(self.comment.path) == 'requests/auth.py'

    def test_position(self):
        expect(self.comment.position) >= 0

    def test_original_position(self):
        expect(self.comment.original_position) == 46

    def test_updated_at(self):
        expect(self.comment.updated_at).isinstance(datetime)

    def test_user(self):
        expect(self.comment.user).isinstance(User)
        expect(self.comment.user.login) == 'idan'

    def test_requires_auth(self):
        self.raisesGHE(self.comment.delete)
        self.raisesGHE(self.comment.edit, 'foo')


class TestPullDestination(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestPullDestination, self).__init__(methodName)
        repo = self.g.repository(self.kr, 'requests')
        self.dest = repo.pull_request(833).base

    def test_pull_destination(self):
        expect(self.dest).isinstance(PullDestination)
        expect(repr(self.dest)) != ''

    def test_direction(self):
        expect(self.dest.direction) == 'Base'

    def test_label(self):
        expect(self.dest.label) == 'kennethreitz:develop'

    def test_sha(self):
        expect(self.dest.sha) == 'c8f166f696327dc8ec07a248863fcc35fafa2038'

    def test_ref(self):
        expect(self.dest.ref) == 'develop'

    def test_repo(self):
        expect(self.dest.repo) == (self.kr, 'requests')

    def test_user(self):
        expect(self.dest.user.login) == self.kr


class TestPullFile(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestPullFile, self).__init__(methodName)
        repo = self.g.repository(self.kr, 'requests')
        self.pf = repo.pull_request(833).list_files()[0]

    def test_file(self):
        expect(self.pf).isinstance(PullFile)
        expect(repr(self.pf)) != ''

    def test_additions(self):
        expect(self.pf.additions) == 2

    def test_blob_url(self):
        expect(self.pf.blob_url).isinstance(str_test)
        expect('blob' in self.pf.blob_url).is_True()
        expect('compat.py' in self.pf.blob_url).is_True()

    def test_changes(self):
        expect(self.pf.changes) == 2

    def test_deletions(self):
        expect(self.pf.deletions) == 0

    def test_filename(self):
        expect(self.pf.filename) == 'requests/compat.py'

    def test_patch(self):
        expect(self.pf.patch).isinstance(str_test)

    def test_raw_url(self):
        expect(self.pf.raw_url) == self.pf.blob_url.replace('blob', 'raw')

    def test_sha(self):
        expect(self.pf.sha) == '351b7c6e03070523b963d9adc71ef2b89a0fa574'

    def test_status(self):
        expect(self.pf.status) == 'modified'
