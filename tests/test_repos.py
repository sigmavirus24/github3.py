import os
import github3
from tests.utils import (generate_response, expect, BaseCase, load)


class TestRepository(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = github3.repos.Repository(load('repo'))

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = github3.repos.Repository(self.repo.to_json(), self.g)
        self.api = 'https://api.github.com/repos/sigmavirus24/github3.py/'

    def test_add_collaborator(self):
        self.request.return_value = generate_response('', 204)
        self.args = ('PUT', self.api + 'collaborators/sigmavirus24')
        self.conf = {'data': None}

        with expect.githuberror():
            self.repo.add_collaborator('foo')

        self.login()
        expect(self.repo.add_collaborator(None)).is_False()
        expect(self.repo.add_collaborator('sigmavirus24')).is_True()
        self.mock_assertions()

    def test_archive(self):
        headers = {'content-disposition': 'filename=foo'}
        self.request.return_value = generate_response('archive', 200,
                                                      **headers)
        self.args = ('GET', self.api + 'tarball/master')
        self.conf.update({'stream': True})

        expect(self.repo.archive(None)).is_False()

        expect(os.path.isfile('foo')).is_False()
        expect(self.repo.archive('tarball')).is_True()
        expect(os.path.isfile('foo')).is_True()
        os.unlink('foo')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        expect(os.path.isfile('path_to_file')).is_False()
        expect(self.repo.archive('tarball', 'path_to_file')).is_True()
        expect(os.path.isfile('path_to_file')).is_True()
        os.unlink('path_to_file')

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.args = ('GET', self.api + 'zipball/randomref')
        expect(self.repo.archive('zipball', ref='randomref')).is_True()
        os.unlink('foo')

    def test_blob(self):
        self.request.return_value = generate_response('blob')
        sha = '3ceb856e2f14e9669fed6384e58c9a1590a2314f'
        self.args = ('GET', self.api + 'git/blobs/' + sha)

        expect(self.repo.blob(sha)).isinstance(github3.git.Blob)
        self.mock_assertions()

    def test_branch(self):
        self.request.return_value = generate_response('branch')
        self.args = ('GET', self.api + 'branches/master')

        expect(self.repo.branch('master')).isinstance(github3.repos.Branch)
        self.mock_assertions()

    def test_commit(self):
        self.request.return_value = generate_response('commit')
        sha = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.args = ('GET', self.api + 'commits/' + sha)

        expect(self.repo.commit(sha)).isinstance(github3.repos.RepoCommit)
        self.mock_assertions()

    def test_commit_comment(self):
        self.request.return_value = generate_response('commit_comment')
        comment_id = 1380832
        self.args = ('GET', self.api + 'comments/{0}'.format(comment_id))

        expect(self.repo.commit_comment(comment_id)
               ).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_compare_commits(self):
        self.request.return_value = generate_response('comparison')
        base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
        head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.args = ('GET', self.api + 'compare/{0}...{1}'.format(base, head))

        expect(self.repo.compare_commits(base, head)
               ).isinstance(github3.repos.Comparison)
        self.mock_assertions()

    def test_contents(self):
        self.request.return_value = generate_response('contents')
        filename = 'setup.py'
        self.args = ('GET', self.api + 'contents/' + filename)

        expect(self.repo.contents(filename)).isinstance(github3.repos.Contents)
        self.mock_assertions()

    def test_create_blob(self):
        self.request.return_value = generate_response('blob', 201)
        content = 'VGVzdCBibG9i\n'
        encoding = 'base64'
        sha = '30f2c645388832f70d37ab2b47eb9ea527e5ae7c'
        self.args = ('POST', self.api + 'git/blobs')
        self.conf = {'data': {'content': content, 'encoding': encoding}}

        with expect.githuberror():
            self.repo.create_blob(content, encoding)

        self.login()
        expect(self.repo.create_blob(None, None)) == ''
        expect(self.repo.create_blob(content, encoding)) == sha
        self.mock_assertions()

    def test_create_comment(self):
        self.request.return_value = generate_response('commit_comment', 201)
        body = ('Late night commits are never a good idea. I refactored a '
                'bit. `User` objects and `Organization` objects share a lot '
                'of common attributes. I turned those common attributes into '
                'one `BaseAccount` class to make things simpler. ')
        sha = 'd41566090114a752eb3a87dbcf2473eb427ef0f3'
        self.args = ('POST', self.api + 'commits/{0}/comments'.format(sha))
        self.conf = {
            'data': {
                'body': body, 'commit_id': sha, 'line': 1, 'path': '',
                'position': 1
            }
        }

        with expect.githuberror():
            self.repo.create_comment(body, sha)

        self.login()
        expect(self.repo.create_comment(None, None)).is_None()
        expect(self.repo.create_comment(body, sha, line=0)).is_None()
        expect(self.repo.create_comment(body, sha)
               ).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_create_commit(self):
        self.request.return_value = generate_response('commit', 201)
        data = {'message': 'My commit message',
                'author': {
                    'name': 'Ian Cordasco',
                    'email': 'foo@example.com',
                    'date': '2008-07-09T16:13:30+12:00',
                },
                'committer': {},
                'parents': [
                    '7d1b31e74ee336d15cbd21741bc88a537ed063a0'
                ],
                'tree': '827efc6d56897b048c772eb4087f854f46256132',
                }
        self.conf = {'data': data}
        self.args = ('POST', self.api + 'git/commits')

        with expect.githuberror():
            self.repo.create_commit(**data)

        self.login()
        expect(self.repo.create_commit(None, None, None)).is_None()
        expect(self.repo.create_commit(**data)).isinstance(github3.git.Commit)
        self.mock_assertions()

    def test_create_download(self):
        pass

    def test_create_fork(self):
        self.request.return_value = generate_response('repo', 202)
        self.conf = {'data': None}
        self.args = ('POST', self.api + 'forks')

        with expect.githuberror():
            self.repo.create_fork()

        self.login()
        expect(self.repo.create_fork()).isinstance(github3.repos.Repository)
        self.mock_assertions()

        self.conf['data'] = {'organization': 'github3py'}
        expect(self.repo.create_fork('github3py')
               ).isinstance(github3.repos.Repository)
        self.mock_assertions()

    def test_create_issue(self):
        self.request.return_value = generate_response('issue', 201)
        title = 'Construct _api attribute on our own'
        self.args = ('POST', self.api + 'issues')
        self.conf = {'data': {'title': title}}

        with expect.githuberror():
            self.repo.create_issue(title)

        self.login()
        expect(self.repo.create_issue(None)).is_None()
        expect(self.repo.create_issue(title)).isinstance(github3.issues.Issue)
        self.mock_assertions()

        body = 'Fake body'
        #self.conf['data'].update(body=body)
        expect(self.repo.create_issue(title, body)
               ).isinstance(github3.issues.Issue)
        self.mock_assertions()

        assignee, mile, labels = 'sigmavirus24', 1, ['bug', 'enhancement']
        #self.conf['data'].update({'assignee': assignee, 'milestone': mile,
        #                          'labels': labels})
        expect(self.repo.create_issue(title, body, assignee, mile, labels)
               ).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_create_key(self):
        self.request.return_value = generate_response('key', 201)
        self.args = ('POST', self.api + 'keys')
        self.conf = {'data': {'key': 'ssh-rsa foobarbogus',
                              'title': 'Fake key'}}

        with expect.githuberror():
            self.repo.create_key(**self.conf['data'])

        self.login()
        expect(self.repo.create_key(None, None)).is_None()
        expect(self.request.called).is_False()
        expect(self.repo.create_key(**self.conf['data'])).isinstance(
            github3.users.Key)
        self.mock_assertions()

    def test_create_label(self):
        self.request.return_value = generate_response('label', 201)
        self.args = ('POST', self.api + 'labels')
        self.conf = {'data': {'name': 'foo', 'color': 'f00f00'}}

        with expect.githuberror():
            self.repo.create_label(**self.conf['data'])

        self.login()
        expect(self.repo.create_label(None, None)).is_None()
        expect(self.request.called).is_False()
        expect(self.repo.create_label(**self.conf['data'])).isinstance(
            github3.issues.Label)
        self.mock_assertions()

    def test_create_milestone(self):
        self.request.return_value = generate_response('milestone', 201)
        self.args = ('POST', self.api + 'milestones')
        self.conf = {'data': {'title': 'foo'}}

        with expect.githuberror():
            self.repo.create_milestone(**self.conf['data'])

        self.login()
        expect(self.repo.create_milestone(None)).is_None()
        expect(self.request.called).is_False()
        expect(self.repo.create_milestone('foo')).isinstance(
            github3.issues.Milestone)
        self.mock_assertions()

    def test_create_pull(self):
        self.request.return_value = generate_response('pull', 201)
        self.args = ('POST', self.api + 'pulls')
        self.conf = {'data': {'title': 'Fake title', 'base': 'master',
                              'head': 'feature_branch'}}

        with expect.githuberror():
            self.repo.create_pull(**self.conf['data'])

        self.login()
        expect(self.repo.create_pull(None, None, None)).is_None()
        expect(self.request.called).is_False()
        expect(self.repo.create_pull(**self.conf['data'])).isinstance(
            github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_pull_from_issue(self):
        self.request.return_value = generate_response('pull', 201)
        self.args = ('POST', self.api + 'pulls')
        self.conf = {'data': {'issue': 1, 'base': 'master',
                              'head': 'feature_branch'}}

        with expect.githuberror():
            self.repo.create_pull_from_issue(**self.conf['data'])

        self.login()
        expect(self.repo.create_pull_from_issue(0, 'foo', 'bar')).is_None()
        expect(self.request.called).is_False()
        expect(self.repo.create_pull_from_issue(**self.conf['data'])
               ).isinstance(github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_ref(self):
        self.request.return_value = generate_response('ref', 201)
        self.args = ('POST', self.api + 'git/refs')
        self.conf = {'data': {'ref': 'refs/heads/master', 'sha': 'fakesha'}}

        with expect.githuberror():
            self.repo.create_ref('foo', 'bar')

        self.login()
        expect(self.repo.create_ref('foo/bar', None)).is_None()
        expect(self.repo.create_ref(**self.conf['data'])).isinstance(
            github3.git.Reference)
        self.mock_assertions()

    def test_create_status(self):
        self.request.return_value = generate_response('status', 201)
        self.args = ('POST', self.api + 'statuses/fakesha')
        self.conf = {'data': {'state': 'success'}}

        with expect.githuberror():
            self.repo.create_status('fakesha', 'success')

        self.login()
        expect(self.repo.create_status(None, None)).is_None()
        expect(self.repo.create_status('fakesha', 'success')).isinstance(
            github3.repos.Status)
        self.mock_assertions()
