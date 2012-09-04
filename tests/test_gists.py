import base
from expecter import expect
import github3
from github3.gists import Gist, GistComment, GistFile
from github3.users import User


class TestGist(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGist, self).__init__(methodName)
        self.gists = self.g.list_gists()
        self.gist = self.gists[0]

    def test_gists_not_empty(self):
        expect(self.gists) != []
        self.expect_list_of_class(self.gists, Gist)

    def test_files(self):
        for g in self.gists:
            expect(g.files) >= 0
            expect(g.list_files()).isinstance(list)
            expect(g.forks) >= 0
            self.assertAreNotNone(g, 'created_at', 'git_pull_url',
                    'git_push_url', 'html_url', 'id')
            expect(g.is_public()).isinstance(bool)
            expect(g.is_starred()).isinstance(bool)
            expect(g.to_json()).isinstance(dict)
            comments = g.list_comments()
            if comments:
                for c in comments:
                    expect(c).isinstance(GistComment)

            expect(g.refresh()).isinstance(bool)

            # if it is not an anonymous gist
            if g.user:
                expect(g.user).isinstance(User)

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            for g in self.gists:
                g.create_comment('Foo')
                g.delete()
                g.edit()
                g.fork()
                g.star()
                g.unstar()


class TestGistFile(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGistFile, self).__init__(methodName)
        self.ninjax = self.g.gist(3156487)
        self.comments = self.ninjax.list_comments()
        self.files = self.ninjax.list_files()
        # A gist I had wrote for someone in #python freenode.
        # It won't be deleted and won't be further updated

    def test_comments(self):
        for c in self.comments:
            expect(c).isinstance(GistComment)
            self.assertAreNotNone(c, 'body', 'body_html', 'body_text',
                    'created_at', 'id', 'user')
            expect(c.user).isinstance(User)
            expect(repr(c)) != ''

    def test_list_not_empty(self):
        expect(self.files) != []

    def test_is_gistfile(self):
        for f in self.files:
            expect(f).isinstance(GistFile)

    def test_files(self):
        for f in self.files:
            expect(f).isinstance(GistFile)
            self.assertAreNotNone(f, 'content', 'name', 'lang', 'raw_url',
                    'size')
            expect(repr(f)) != ''

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            for c in self.comments:
                c.delete()
                c.edit('foo')
