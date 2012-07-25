import base
from expecter import expect
import github3
from github3.github import Gist


class TestGist(base.BaseTest):
    def test_comments(self):
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

            with expect.raises(github3.GitHubError):
                g.create_comment('Foo')
                g.delete()
                g.edit()
                g.fork()
