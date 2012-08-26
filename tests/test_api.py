import base
import github3
from base import expect


class TestAPI(base.BaseTest):
    def test_gist(self):
        expect(github3.gist(3156487)).isinstance(github3.gists.Gist)

    def test_list_gists(self):
        list_gists = github3.list_gists
        self.expect_list_of_class(list_gists(), github3.gists.Gist)
        self.expect_list_of_class(list_gists(self.sigm), github3.gists.Gist)

    def test_list_followers(self):
        self.expect_list_of_class(github3.list_followers(self.sigm),
                github3.users.User)

    def test_list_following(self):
        self.expect_list_of_class(github3.list_following(self.sigm),
                github3.users.User)

    def test_list_repo_issues(self):
        self.expect_list_of_class(github3.list_repo_issues(self.sigm,
            self.todo, state='closed'), github3.issues.Issue)

    def test_issue(self):
        expect(github3.issue(self.sigm, self.todo, 1))

    def test_list_events(self):
        self.expect_list_of_class(github3.list_events(), github3.events.Event)

    def test_markdown(self):
        f = ['<h1>\n<a name="header-1" class="anchor" href="#header-1">',
            '<span class="mini-icon mini-icon-link"></span>',
            '</a>Header 1</h1>\n\n<h2>\n',
            '<a name="paragraph" class="anchor" href="#paragraph">',
            '<span class="mini-icon mini-icon-link"></span></a>Paragraph</h2>',
            '\n\n<h1>\n<a name="header-2" class="anchor" href="#header-2">',
            '<span class="mini-icon mini-icon-link"></span>',
            '</a>Header 2</h1>\n\n<p>Paragraph</p>']
        f = ''.join(f)
        s = github3.markdown(
                '# Header 1\n\nParagraph\n------\n# Header 2\n\nParagraph'
                )
        expect(str(s)) == f

    def test_organization(self):
        expect(github3.organization(self.gh3py)).isinstance(
                github3.orgs.Organization
                )

    def test_repository(self):
        expect(github3.repository(self.sigm, self.todo)).isinstance(
                github3.repos.Repository
                )

    def test_search_issues(self):
        self.expect_list_of_class(github3.search_issues(
            self.sigm, self.todo, 'closed', 'addons'
            ), github3.legacy.LegacyIssue)

    def test_search_users(self):
        self.expect_list_of_class(github3.search_users('kenneth'),
                github3.legacy.LegacyUser)

    def test_search_email(self):
        expect(github3.search_email('graffatcolmingov@gmail.com')).isinstance(
                github3.legacy.LegacyUser)

    def test_user(self):
        expect(github3.user(self.sigm)).isinstance(github3.users.User)

    def test_ratelimit_remaining(self):
        expect(github3.ratelimit_remaining()) > 0
