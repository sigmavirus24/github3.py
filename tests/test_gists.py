from .base import BaseTest, expect, str_test
from datetime import datetime
import github3
from github3.gists import Gist, GistComment, GistFile
from github3.users import User


class TestGist(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGist, self).__init__(methodName)
        self.gists = self.g.list_gists()
        self.gist = self.gists[0]

    def test_gists_not_empty(self):
        expect(self.gists) != []
        expect(self.gists).list_of(Gist)

    def test_repr(self):
        expect(repr(self.gist)) != ''

    def test_list_forks(self):
        expect(self.gist.list_forks()).isinstance(list)

    def test_updated_at(self):
        expect(self.gist.updated_at).isinstance(datetime)

    def test_files(self):
        expect(self.gist.files) >= 0

    def test_list_files(self):
        expect(self.gist.list_files()).isinstance(list)

    def test_forks(self):
        expect(self.gist.forks) >= 0

    def test_created_at(self):
        expect(self.gist.created_at).isinstance(datetime)

    def test_git_pull_url(self):
        expect(self.gist.git_pull_url).isinstance(str_test)
        expect(self.gist.git_pull_url) != ''

    def test_git_push_url(self):
        expect(self.gist.git_push_url).isinstance(str_test)
        expect(self.gist.git_push_url) != ''

    def test_html_url(self):
        expect(self.gist.html_url).isinstance(str_test)
        expect(self.gist.html_url) != ''

    def test_id(self):
        expect(self.gist.id) >= str(0)

    def test_is_public(self):
        expect(self.gist.is_public()).isinstance(bool)

    def test_is_starred(self):
        expect(self.gist.is_starred()).isinstance(bool)

    def test_to_json(self):
        expect(self.gist.to_json()).isinstance(dict)

    def test_iter_comments(self):
        comments = [c for c in self.gist.iter_comments(1)]
        expect(comments).list_of(GistComment)

    def test_list_comments(self):
        try:
            expect(self.gist.list_comments()).list_of(GistComment)
        except github3.GitHubError:
            pass

    def test_refresh(self):
        expect(self.gist.refresh()).isinstance(bool)

        # if it is not an anonymous gist
    def test_user(self):
        if self.gist.user:
            expect(self.gist.user).isinstance(User)

    def test_requires_auth(self):
        for g in self.gists:
            self.raisesGHE(g.create_comment, 'Foo')
            self.raisesGHE(g.delete)
            self.raisesGHE(g.edit)
            self.raisesGHE(g.fork)
            self.raisesGHE(g.star)
            self.raisesGHE(g.unstar)

    def test_with_auth(self):
        if not self.auth:
            return
        gist = self._g.gist(self.gist.id)
        expect(gist.star()).is_True()
        expect(gist.unstar()).is_True()
        my_gist = gist.fork()
        expect(my_gist).isinstance(Gist)
        files = {'test.txt': 'testing github3.py'}
        expect(my_gist.edit(files=files)).is_True()
        expect(my_gist.edit(description='foo')).is_True()
        expect(my_gist.edit()).is_False()
        expect(my_gist.create_comment('foo bar bogus')).is_not_None()
        expect(my_gist.delete()).is_True()


class TestGistFile(BaseTest):
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
            self.assertAreNotNone(f, 'content', 'name', 'language', 'raw_url',
                    'size')
            expect(repr(f)) != ''

    def test_requires_auth(self):
        for c in self.comments:
            self.raisesGHE(c.delete)
            self.raisesGHE(c.edit, 'foo')
