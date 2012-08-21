import base
from expecter import expect
import github3
from github3.gists import Gist, GistComment, GistFile
from github3.users import User


class TestGist(base.BaseTest):
    def test_gists(self):
        gists = self.g.list_gists()
        expect(gists) != []

        for g in gists:
            expect(g).isinstance(Gist)
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
            expect(g.user).isinstance(User)

            with expect.raises(github3.GitHubError):
                g.create_comment('Foo')
                g.delete()
                g.edit()
                g.fork()
                g.star()
                g.unstar()

    def test_files(self):
        ninjax = self.g.gist(3156487)  # An gist I used for someone in
        ##python on freenode. I promise not to update it further
        expect(ninjax.files) == 2
        coms = ninjax.list_comments()
        if coms:
            for c in coms:
                expect(c).isinstance(GistComment)
                self.assertAreNotNone(c, 'body', 'body_html', 'body_text',
                        'created_at', 'id', 'user')
                with expect.raises(github3.GitHubError):
                    c.delete()
                    c.edit('foo')

        files = ninjax.list_files()
        expect(files) != []
        for f in files:
            expect(f).isinstance(GistFile)
            self.assertAreNotNone(f, 'content', 'name', 'lang', 'raw_url',
                    'size')
