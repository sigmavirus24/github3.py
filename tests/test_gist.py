import base
from expecter import expect
import github3
from github3 import Gist, GistComment


class TestGist(base.BaseTest):
    def test_gists(self):
        gists = self.g.list_gists()
        expect(gists) != []

        for g in gists:
            expect(g).isinstance(Gist)
            self.assertIsNotNone(g.created_at)
            self.assertIsNotNone(g.description)
            expect(g.files) != []
            expect(g.forks) >= 0
            self.assertIsNotNone(g.git_pull_url)
            self.assertIsNotNone(g.git_push_url)
            self.assertIsNotNone(g.html_url)
            expect(g.id) >= 1
            expect(g.is_public()).isinstance(bool)
            expect(g.is_starred()).isinstance(bool)
            comments = g.list_comments()
            if comments:
                for c in comments:
                    expect(c).isinstance(GistComment)

            with expect.raises(github3.GitHubError):
                g.create_comment('Foo')
                g.delete()
                g.edit()
                g.fork()
