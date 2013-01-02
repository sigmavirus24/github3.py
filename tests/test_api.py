import github3
from tests.utils import APITestMixin


class TestAPI(APITestMixin):
    def test_authorize(self):
        args = ('login', 'password', ['scope1'], 'note', 'note_url.com', '',
                '')
        github3.authorize(*args)
        self.gh.authorize.assert_called_with(*args)

    def test_login(self):
        pass

    def test_gist(self):
        args = (123,)
        github3.gist(*args)
        self.gh.gist.assert_called_with(*args)

    def test_gitignore_template(self):
        args = ('Python',)
        github3.gitignore_template(*args)
        self.gh.gitignore_template.assert_called_with(*args)

    def test_gitignore_templates(self):
        github3.gitignore_templates()
        assert self.gh.gitignore_templates.called is True

    def test_iter_all_repos(self):
        github3.iter_all_repos()
        self.gh.iter_all_repos.assert_called_with(-1)

    def test_iter_all_users(self):
        github3.iter_all_users()
        self.gh.iter_all_users.assert_called_with(-1)

    def test_iter_events(self):
        github3.iter_events()
        self.gh.iter_events.assert_called_with(-1)

    def test_iter_followers(self):
        github3.iter_followers('login')
        self.gh.iter_followers.assert_called_with('login', -1)

    def test_iter_following(self):
        github3.iter_following('login')
        self.gh.iter_following.assert_called_with('login', -1)

    def test_iter_gists(self):
        github3.iter_gists()
        self.gh.iter_gists.assert_called_with(None, -1)

    def test_iter_repo_issues(self):
        args = ('owner', 'repository', '', '', '', '', '', '', -1)
        github3.iter_repo_issues(*args)
        self.gh.iter_repo_issues.assert_called_with(*args)

    def test_iter_orgs(self):
        args = ('login', -1)
        github3.iter_orgs(*args)
        self.gh.iter_orgs.assert_called_with(*args)
