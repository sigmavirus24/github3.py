import pytest

from github3 import GitHubEnterprise, GitHubError
from github3.github import GitHub, GitHubStatus
from github3.projects import Project

from . import helper


def url_for(path=''):
    """Simple function to generate URLs with the base GitHub URL."""
    return 'https://api.github.com/' + path.strip('/')


enterprise_url_for = helper.create_url_helper('https://enterprise.github3.com')


class TestGitHub(helper.UnitHelper):
    described_class = GitHub
    example_data = None

    def test_activate_membership(self):
        self.instance.activate_membership('github3py')
        self.session.patch.assert_called_once_with(
            url_for('user/memberships/orgs/github3py'),
            data='{"state": "active"}'
        )

    def test_add_email_addresses(self):
        """Verify request to add email addresses for a user."""
        self.instance.add_email_addresses(['example1@example.com',
                                           'example2@example.com'])

        self.post_called_with(
            url_for('user/emails'),
            data=['example1@example.com', 'example2@example.com'],
        )

    def test_add_email_addresses_with_empty_list(self):
        """Verify no request is sent for an empty list of addresses."""
        self.instance.add_email_addresses([])

        assert self.session.post.called is False

    def test_authorization(self):
        """Show that a user can retrieve a specific authorization by id."""
        self.instance.authorization(10)

        self.session.get.assert_called_once_with(
            url_for('authorizations/10'),
        )

    def test_authorize_without_scope(self):
        """Show an authorization can be created for a user without scope."""
        self.instance.authorize('username', 'password')
        self.session.temporary_basic_auth.assert_called_once_with(
            'username', 'password'
        )
        self.post_called_with(
            url_for('authorizations'),
            data={'note': '', 'note_url': '', 'client_id': '',
                  'client_secret': ''}
        )

    def test_authorize(self):
        """Show an authorization can be created for a user."""
        self.instance.authorize('username', 'password', ['user', 'repo'])

        self.session.temporary_basic_auth.assert_called_once_with(
            'username', 'password'
        )
        self.post_called_with(
            url_for('authorizations'),
            data={'note': '', 'note_url': '', 'client_id': '',
                  'client_secret': '', 'scopes': ['user', 'repo']}
        )

    def test_check_authorization(self):
        """Test an app's ability to check a authorization token."""
        self.instance.set_client_id('client-id', 'client-secret')
        self.instance.check_authorization('super-fake-access-token')

        self.session.get.assert_called_once_with(
            url_for('applications/client-id/tokens/super-fake-access-token'),
            params={'client_id': None, 'client_secret': None},
            auth=('client-id', 'client-secret')
        )

    def test_create_gist(self):
        """Test the request to create a gist."""
        self.instance.create_gist('description', {
            'example.py': {'content': '# example contents'}
        })

        self.post_called_with(
            url_for('gists'),
            data={
                'description': 'description',
                'files': {
                    'example.py': {
                        'content': '# example contents'
                    }
                },
                'public': True,
            }
        )

    def test_create_gpg_key(self):
        """Test the request to create a GPG key."""
        self.instance.create_gpg_key('GPG key text')

        self.session.post.assert_called_once_with(
            url_for('user/gpg_keys'),
            '{"armored_public_key": "GPG key text"}'
        )

    def test_create_key(self):
        """Test the request to create a key."""
        self.instance.create_key('key_name', 'key text', read_only=False)

        self.post_called_with(
            url_for('user/keys'),
            data={
                'title': 'key_name',
                'key': 'key text',
                'read_only': False
            }
        )

    def test_create_key_with_readonly(self):
        """ Test the request to create a key with read only"""
        self.instance.create_key('key_name', 'key text', read_only=True)

        self.post_called_with(
            url_for('user/keys'),
            data={
                'title': 'key_name',
                'key': 'key text',
                'read_only': True
            }
        )

    def test_create_key_requires_a_key(self):
        """Test that no request is made with an empty key."""
        self.instance.create_key('title', '')

        assert self.session.post.called is False

    def test_create_key_requires_a_title(self):
        """Test that no request is made with an empty title."""
        self.instance.create_key('', 'key text')

        assert self.session.post.called is False

    def test_create_repository(self):
        """Test the request to create a repository."""
        self.instance.create_repository('repo-name')

        self.post_called_with(
            url_for('user/repos'),
            data={
                'name': 'repo-name',
                'description': '',
                'homepage': '',
                'private': False,
                'has_issues': True,
                'has_wiki': True,
                'auto_init': False,
                'gitignore_template': ''
            }
        )

    def test_delete_email_addresses(self):
        """Verify the request to delete a user's email addresses."""
        self.instance.delete_email_addresses(['example1@example.com',
                                              'example2@example.com'])

        self.delete_called_with(
            url_for('user/emails'),
            data=['example1@example.com', 'example2@example.com'],
        )

    def test_emojis(self):
        """Test the request to retrieve GitHub's emojis."""
        self.instance.emojis()

        self.session.get.assert_called_once_with(url_for('emojis'))

    def test_feeds(self):
        self.instance.feeds()

        self.session.get.assert_called_once_with(url_for('feeds'))

    def test_follow(self):
        """Test the request to follow a user."""
        self.instance.follow('username')

        self.session.put.assert_called_once_with(
            url_for('user/following/username')
        )

    def test_follow_requires_a_username(self):
        """Test that GitHub#follow requires a username."""
        self.instance.follow(None)

        assert self.session.put.called is False

    def test_gist(self):
        """Test the request to retrieve a specific gist."""
        self.instance.gist(10)

        self.session.get.assert_called_once_with(url_for('gists/10'))

    def test_gitignore_template(self):
        """Test the request to retrieve a gitignore template."""
        self.instance.gitignore_template('Python')

        self.session.get.assert_called_once_with(
            url_for('gitignore/templates/Python')
        )

    def test_gitignore_templates(self):
        """Test the request to retrieve gitignore templates."""
        self.instance.gitignore_templates()

        self.session.get.assert_called_once_with(
            url_for('gitignore/templates')
        )

    def test_gpg_key(self):
        """Verify the request to retrieve a GPG key."""
        self.instance.gpg_key(3)

        self.session.get.assert_called_once_with(url_for('user/gpg_keys/3'))

    def test_is_following(self):
        """Test the request to check if the user is following a user."""
        self.instance.is_following('username')

        self.session.get.assert_called_once_with(
            url_for('user/following/username')
        )

    def test_is_starred(self):
        """Test the request to check if the user starred a repository."""
        self.instance.is_starred('username', 'repository')

        self.session.get.assert_called_once_with(
            url_for('user/starred/username/repository')
        )

    def test_is_starred_requires_an_owner(self):
        """Test that GitHub#is_starred requires an owner."""
        self.instance.is_starred(None, 'repo')

        assert self.session.get.called is False

    def test_is_starred_requires_a_repo(self):
        """Test that GitHub#is_starred requires an repo."""
        self.instance.is_starred('username', None)

        assert self.session.get.called is False

    def test_issue(self):
        """Test the request to retrieve a single issue."""
        self.instance.issue('owner', 'repo', 1)

        self.session.get.assert_called_once_with(
            url_for('repos/owner/repo/issues/1')
        )

    def test_issue_requires_username(self):
        """Test GitHub#issue requires a non-None username."""
        self.instance.issue(None, 'foo', 1)

        assert self.session.get.called is False

    def test_issue_requires_repository(self):
        """Test GitHub#issue requires a non-None repository."""
        self.instance.issue('foo', None, 1)

        assert self.session.get.called is False

    def test_issue_requires_positive_issue_id(self):
        """Test GitHub#issue requires positive issue id."""
        self.instance.issue('foo', 'bar', -1)

        assert self.session.get.called is False

    def test_key(self):
        """Verify request for retrieving a user's key."""
        self.instance.key(1)
        self.session.get.assert_called_once_with(
            url_for('user/keys/1')
        )

    def test_key_negative_id(self):
        """Verify request for retrieving a user's key."""
        self.instance.key(-1)
        self.session.get.called is False

    def test_license(self):
        """Verify the request to retrieve a license."""
        self.instance.license('MIT')

        self.session.get.assert_called_once_with(url_for('licenses/MIT'))

    def test_login(self):
        """Verify the request for user logging in."""
        self.instance.login('user', 'password')
        self.session.basic_auth.assert_called_once_with(
            'user',
            'password'
        )

        self.session.two_factor_auth_callback.assert_called_once_with(None)

    def test_login_with_token(self):
        """Verify the request for user logging in."""
        token = 'OauthToken'

        def _callback(x):
            return x

        callback = _callback
        self.instance.login(token=token, two_factor_callback=callback)
        self.session.token_auth.assert_called_once_with(token)
        self.session.two_factor_auth_callback.assert_called_once_with(
            callback
        )

    def test_markdown(self):
        """Verify the request for rendering a markdown document."""
        self.session.post.return_value = helper.mock.Mock(
            ok=True
        )
        text = '##Hello'
        mode = 'markdown'
        self.instance.markdown(text=text, mode=mode)
        self.post_called_with(
            url_for('markdown'),
            data={
                'text': text,
                'mode': mode
            },
            headers={},
        )

    def test_markdown_raw(self):
        """Verify the request for rendering a markdown document."""
        self.session.post.return_value = helper.mock.Mock(
            ok=True
        )
        text = 'Hello'
        raw = True
        self.instance.markdown(text=text, raw=raw)
        self.session.post.assert_called_once_with(
            url_for('markdown/raw'),
            'Hello',
            headers={
                'content-type': 'text/plain'
            }
        )

    def test_markdown_gfm(self):
        """Verify the request for rendering a markdown document."""
        self.session.post.return_value = helper.mock.Mock(
            ok=True
        )
        text = '##Hello'
        mode = 'gfm'
        context = 'sigmavirus24/github3.py'
        self.instance.markdown(text=text, mode=mode, context=context)
        self.post_called_with(
            url_for('markdown'),
            data={
                'text': text,
                'mode': mode,
                'context': context
            },
            headers={},
        )

    def test_me(self):
        """Test the ability to retrieve the authenticated user's info."""
        self.instance.me()

        self.session.get.assert_called_once_with(url_for('user'))

    def test_meta(self):
        """Verify the request for returning  incoming service hooks data."""
        self.instance.meta()
        self.session.get.assert_called_once_with(
            url_for('meta')
        )

    def test_octocat(self):
        """Verify the request for retrieving an easter egg."""
        self.session.get.return_value = helper.mock.Mock(
            ok=True, text='egg'
        )
        egg = self.instance.octocat(say='hello')
        self.session.get.assert_called_once_with(
            url_for('octocat'),
            params={
                's': 'hello'
            }
        )

        assert egg == 'egg'

    def test_octocat_response_not_ok(self):
        """Verify the request for retrieving an easter egg."""
        self.session.get.return_value = helper.mock.Mock(
            ok=False, text='egg'
        )

        egg = self.instance.octocat(say='hello')

        assert egg == ''

    def test_organization(self):
        """Verify the request for retrieving an organization."""
        self.instance.organization(username='github3py')
        self.session.get.assert_called_once_with(
            url_for('orgs/github3py')
        )

    def test_project(self):
        """Test the ability to retrieve a project by its id."""
        self.instance.project(400543)

        self.session.get.assert_called_once_with(
            url_for('projects/400543'),
            headers=Project.CUSTOM_HEADERS
        )

    def test_project_card(self):
        """Test the ability to retrieve a project card by its id."""
        self.instance.project_card(2665856)

        self.session.get.assert_called_once_with(
            url_for('projects/columns/cards/2665856'),
            headers=Project.CUSTOM_HEADERS
        )

    def test_project_column(self):
        """Test the ability to retrieve a project column by its id."""
        self.instance.project_column(957217)

        self.session.get.assert_called_once_with(
            url_for('projects/columns/957217'),
            headers=Project.CUSTOM_HEADERS
        )

    def test_pubsubhubbub(self):
        """Verify the request for creating a pubsubhubbub hook."""
        topic = (
            'hub.topic',
            'https://github.com/octocat/hello-world/events/push'
        )
        body = [('hub.mode', 'subscribe'),
                topic,
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        self.session.post.assert_called_once_with(
            url_for('hub'),
            body,
            headers={
                'Content-Type':
                'application/x-www-form-urlencoded'
            }
        )

    def test_pubsubhubbub_invalid_username(self):
        """Verify a valid call with invalid username does not call post."""
        topic = (
            'hub.topic',
            'https://github.com/-octocat/hello-world/events/push'
        )
        body = [('hub.mode', 'subscribe'),
                topic,
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is False

    def test_pubsubhubbub_valid_username(self):
        """Verify a valid call with valid username calls post."""
        topic = (
            'hub.topic',
            'https://github.com/o-cto-ca-t/hello-world/events/push'
        )
        body = [('hub.mode', 'subscribe'),
                topic,
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is True

    def test_pubsubhubbub_secret(self):
        """Verify the request for creating a pubsubhubbub hook."""
        topic = (
            'hub.topic',
            'https://github.com/octocat/hello-world/events/push'
        )
        body = [('hub.mode', 'subscribe'),
                topic,
                ('hub.callback', 'https://localhost/post'),
                ('hub.secret', 'secret')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        self.session.post.assert_called_once_with(
            url_for('hub'),
            body,
            headers={
                'Content-Type':
                'application/x-www-form-urlencoded'
            }
        )

    def test_pubsubhubbub_required_callback(self):
        """Verify the request for creating a pubsubhubbub hook."""
        topic = (
            'hub.topic',
            'https://github.com/octocat/hello-world/events/push'
        )
        body = [('hub.mode', 'subscribe'),
                topic,
                ('hub.callback', '')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is False

    def test_pubsubhubbub_required_mode(self):
        """Verify the request for creating a pubsubhubbub hook."""
        topic = (
            'hub.topic',
            'https://github.com/octocat/hello-world/events/push'
        )
        body = [('hub.mode', ''),
                topic,
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is False

    def test_pubsubhubbub_required_topic(self):
        """Verify the request for creating a pubsubhubbub hook."""
        body = [('hub.mode', ''),
                ('hub.topic', ''),
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is False

    def test_pubsubhubbub_topic_no_match(self):
        """Verify the request for creating a pubsubhubbub hook."""
        body = [('hub.mode', 'subscribe'),
                ('hub.topic', ''),
                ('hub.callback', 'https://localhost/post')]
        data = dict([(k[4:], v) for k, v in body])
        self.instance.pubsubhubbub(**data)
        assert self.session.post.called is False

    def test_pull_request(self):
        """Verify the request for retrieving a pull request."""
        self.instance.pull_request(owner='octocat',
                                   repository='hello-world',
                                   number=1)

        self.session.get.assert_called_once_with(
            url_for('repos/octocat/hello-world/pulls/1')
        )

    def test_pull_request_negative_id(self):
        """Verify the request for retrieving a pull request."""
        self.instance.pull_request(owner='octocat',
                                   repository='hello-world',
                                   number=-1)

        self.session.get.called is False

    def test_repository(self):
        """Verify the GET request for a repository."""
        self.instance.repository('user', 'repo')

        self.session.get.assert_called_once_with(url_for('repos/user/repo'))

    def test_repository_with_invalid_repo(self):
        """Verify there is no call made for invalid repo combos."""
        self.instance.repository('user', None)

        assert self.session.get.called is False

    def test_repository_with_invalid_user(self):
        """Verify there is no call made for invalid username combos."""
        self.instance.repository(None, 'repo')

        assert self.session.get.called is False

    def test_repository_with_invalid_user_and_repo(self):
        """Verify there is no call made for invalid user/repo combos."""
        self.instance.repository(None, None)

        assert self.session.get.called is False

    def test_repository_with_id(self):
        """Test the ability to retrieve a repository by its id."""
        self.instance.repository_with_id(10)

        self.session.get.assert_called_once_with(url_for('repositories/10'))

    def test_repository_with_id_requires_a_positive_id(self):
        """Test the ability to retrieve a repository by its id."""
        self.instance.repository_with_id(-10)

        assert self.session.get.called is False

    def test_repository_with_id_accepts_a_string(self):
        """Test the ability to retrieve a repository by its id."""
        self.instance.repository_with_id('10')

        self.session.get.assert_called_once_with(url_for('repositories/10'))

    def test_set_client_id(self):
        """Test the ability to set client id/secret."""
        auth = ('id000000000000000000', 'secret99999999999999')
        self.instance.set_client_id(*auth)
        assert self.session.params['client_id'] == auth[0]
        assert self.session.params['client_secret'] == auth[1]

    def test_two_factor_login(self):
        """Test the ability to pass two_factor_callback."""
        self.instance.login('username', 'password',
                            two_factor_callback=lambda *args: 'foo')

    def test_can_login_without_two_factor_callback(self):
        """Test that two_factor_callback is not required."""
        self.instance.login('username', 'password')
        self.instance.login(token='token')

    def test_unfollow(self):
        """Verify the request for unfollowing a user."""
        self.instance.unfollow('sigmavirus24')
        self.session.delete.assert_called_once_with(
            url_for('user/following/sigmavirus24')
        )

    def test_unfollow_required_username(self):
        """Verify the request for unfollowing a user."""
        self.instance.unfollow('')
        self.session.delete.called is False

    def test_unstar(self):
        """Verify the request for unstarring a repository."""
        self.instance.unstar('sigmavirus24', 'github3.py')
        self.session.delete.assert_called_once_with(
            url_for('user/starred/sigmavirus24/github3.py')
        )

    def test_unstar_requires_username(self):
        """Verify the request for unstarring a repository."""
        self.instance.unstar('', 'github3.py')
        self.session.delete.called is False

    def test_unstar_requires_repository(self):
        """Verify the request for unstarring a repository."""
        self.instance.unstar('sigmavirus24', '')
        self.session.delete.called is False

    def test_unstar_requires_username_and_repository(self):
        """Verify the request for unstarring a repository."""
        self.instance.unstar('', '')
        self.session.delete.called is False

    def test_update_me(self):
        """Verify the request to update the authenticated user's profile."""
        self.instance.update_me(name='New name', email='email@example.com',
                                blog='http://blog.example.com', company='Corp',
                                location='here')

        self.patch_called_with(
            url_for('user'),
            data={'name': 'New name', 'email': 'email@example.com',
                  'blog': 'http://blog.example.com', 'company': 'Corp',
                  'location': 'here', 'hireable': False}
            )

    def test_user(self):
        """Test that a user can retrieve information about any user."""
        self.instance.user('username')

        self.session.get.assert_called_once_with(
            url_for('users/username'),
        )

    def test_user_with_id(self):
        """Test that any user's information can be retrieved by id."""
        self.instance.user_with_id(10)

        self.session.get.assert_called_once_with(url_for('user/10'))

    def test_user_with_id_requires_a_positive_id(self):
        """Test that user_with_id requires a positive parameter."""
        self.instance.user_with_id(-10)

        assert self.session.get.called is False

    def test_user_with_id_accepts_a_string(self):
        """Test that any user's information can be retrieved by id."""
        self.instance.user_with_id('10')

        self.session.get.assert_called_once_with(url_for('user/10'))

    def test_set_user_agent_required_user_agent(self):
        self.instance.set_user_agent('')

        self.session.headers.update.called is False

    def test_set_user_agent(self):
        self.instance.set_user_agent('github3py')
        self.session.headers.update.assert_called_once_with({
            'User-Agent': 'github3py'
        })

    def test_star_required_username_and_repo(self):
        assert self.instance.star(username='', repo='') is False

    def test_star_required_repo(self):
        assert self.instance.star(username='sigmavirus24', repo='') is False

    def test_star_required_username(self):
        assert self.instance.star(username='', repo='github3.py') is False

    def test_star(self):
        """Verify the request for starring a repository."""
        self.instance.star('sigmavirus24', 'github3.py')

        self.session.put.assert_called_once_with(
            url_for('user/starred/sigmavirus24/github3.py')
        )

    def test_zen(self):
        """Verify the request for returning a quote from Zen of Github."""
        self.session.get.return_value = helper.mock.Mock(
            status_code=200, text='hello'
        )
        self.instance.zen()
        self.session.get.assert_called_once_with(
            url_for('zen')
        )


class TestGitHubIterators(helper.UnitIteratorHelper):
    described_class = GitHub
    example_data = None

    def test_all_events(self):
        """Show that one can iterate over all public events."""
        i = self.instance.all_events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_all_organizations(self):
        """Show that one can iterate over all organizations."""
        i = self.instance.all_organizations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('organizations'),
            params={'per_page': 100},
            headers={}
        )

    def test_all_organizations_per_page(self):
        """Show that one can iterate over all organizations with per_page."""
        i = self.instance.all_organizations(per_page=25)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('organizations'),
            params={'per_page': 25},
            headers={}
        )

    def test_all_organizations_since(self):
        """Show that one can limit the organizations returned."""
        since = 100000
        i = self.instance.all_organizations(since=since)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('organizations'),
            params={'per_page': 100, 'since': since},
            headers={}
        )

    def test_all_repositories(self):
        """Show that one can iterate over all repositories."""
        i = self.instance.all_repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repositories'),
            params={'per_page': 100},
            headers={}
        )

    def test_all_repositories_per_page(self):
        """Show that one can iterate over all repositories with per_page."""
        i = self.instance.all_repositories(per_page=25)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repositories'),
            params={'per_page': 25},
            headers={}
        )

    def test_all_repositories_since(self):
        """Show that one can limit the repositories returned."""
        since = 100000
        i = self.instance.all_repositories(since=since)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repositories'),
            params={'per_page': 100, 'since': since},
            headers={}
        )

    def test_all_users(self):
        """Show that one can iterate over all users."""
        i = self.instance.all_users()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users'),
            params={'per_page': 100},
            headers={}
        )

    def test_all_users_per_page(self):
        """Show that one can iterate over all users with per_page."""
        i = self.instance.all_users(per_page=25)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users'),
            params={'per_page': 25},
            headers={}
        )

    def test_all_users_since(self):
        """Show that one can limit the users returned."""
        since = 100000
        i = self.instance.all_users(since=since)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users'),
            params={'per_page': 100, 'since': since},
            headers={}
        )

    def test_authorizations(self):
        """
        Show that an authenticated user can iterate over their authorizations.
        """
        i = self.instance.authorizations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('authorizations'),
            params={'per_page': 100},
            headers={}
        )

    def test_emails(self):
        """Show that an authenticated user can iterate over their emails."""
        i = self.instance.emails()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/emails'),
            params={'per_page': 100},
            headers={}
        )

    def test_followers(self):
        """
        Show that an authenticated user can iterate over their followers.
        """
        i = self.instance.followers()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/followers'),
            params={'per_page': 100},
            headers={}
        )

    def test_followers_require_auth(self):
        """Show that one needs to authenticate to use #followers."""
        self.session.has_auth.return_value = False
        with pytest.raises(GitHubError):
            self.instance.followers()

    def test_followers_of(self):
        """Show that one can authenticate over the followers of a user."""
        i = self.instance.followers_of('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/followers'),
            params={'per_page': 100},
            headers={}
        )

    def test_following(self):
        """
        Show that an authenticated user can iterate the users they are
        following.
        """
        i = self.instance.following()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/following'),
            params={'per_page': 100},
            headers={}
        )

    def test_following_require_auth(self):
        """Show that one needs to authenticate to use #following."""
        self.session.has_auth.return_value = False
        with pytest.raises(GitHubError):
            self.instance.following()

    def test_followed_by(self):
        """
        Show that one can authenticate over the users followed by another.
        """
        i = self.instance.followed_by('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/following'),
            params={'per_page': 100},
            headers={}
        )

    def test_gists(self):
        """Show that an authenticated user can iterate over their gists."""
        i = self.instance.gists()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('gists'),
            params={'per_page': 100},
            headers={}
        )

    def test_gists_by(self):
        """Show that an user's gists can be iterated over."""
        i = self.instance.gists_by('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/gists'),
            params={'per_page': 100},
            headers={}
        )

    def test_gpg_keys(self):
        """Verify the request to iterate over the GPG keys."""
        i = self.instance.gpg_keys()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/gpg_keys'),
            params={'per_page': 100},
            headers={}
        )

    def test_issues(self):
        """Show that an authenticated user can iterate over their issues."""
        i = self.instance.issues()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('issues'),
            params={'per_page': 100},
            headers={}
        )

    def test_issues_with_params(self):
        """Show that issues can be filtered."""
        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        p = {'per_page': 100}
        p.update(params)

        i = self.instance.issues(**params)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('issues'),
            params=p,
            headers={}
        )

    def test_keys(self):
        """
        Show that an authenticated user can iterate over their public keys.
        """
        i = self.instance.keys()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/keys'),
            params={'per_page': 100},
            headers={}
        )

    def test_licenses(self):
        """Verify the request to retrieve all licenses."""
        i = self.instance.licenses()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('licenses'),
            params={'per_page': 100},
            headers={}
        )

    def test_notifications(self):
        """
        Show that an authenticated user can iterate over their notifications.
        """
        i = self.instance.notifications()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('notifications'),
            params={'per_page': 100},
            headers={},
        )

    def test_notifications_participating_in(self):
        """Show that the user can filter by pariticpating."""
        i = self.instance.notifications(participating=True)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('notifications'),
            params={'per_page': 100, 'participating': 'true'},
            headers={}
        )

    def test_notifications_all(self):
        """Show that the user can iterate over all of their notifications."""
        i = self.instance.notifications(all=True)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('notifications'),
            params={'per_page': 100, 'all': 'true'},
            headers={}
        )

    def test_organization_issues(self):
        """Show that one can iterate over an organization's issues."""
        i = self.instance.organization_issues('org')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('orgs/org/issues'),
            params={'per_page': 100},
            headers={}
        )

    def test_organization_issues_with_params(self):
        """Show that one can pass parameters to #organization_issues."""
        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        i = self.instance.organization_issues('org', **params)
        self.get_next(i)

        p = {'per_page': 100}
        p.update(params)

        self.session.get.assert_called_once_with(
            url_for('orgs/org/issues'),
            params=p,
            headers={}
        )

    def test_organizations(self):
        """
        Show that one can iterate over all of the authenticated user's orgs.
        """
        i = self.instance.organizations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/orgs'),
            params={'per_page': 100},
            headers={}
        )

    def test_organizations_with(self):
        """Show that one can iterate over all of a user's orgs."""
        i = self.instance.organizations_with('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/orgs'),
            params={'per_page': 100},
            headers={}
        )

    def test_public_gists(self):
        """Show that all public gists can be iterated over."""
        i = self.instance.public_gists()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('gists/public'),
            params={'per_page': 100},
            headers={}
        )

    def test_public_gists_since(self):
        """Show that public gists can be filtered by date."""
        since = '2018-07-13T00:00:00Z'
        i = self.instance.public_gists(since=since)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('gists/public'),
            params={'per_page': 100, 'since': since},
            headers={}
        )

    def test_repository_invitations(self):
        """Verify the request to iterate over the repository invitations."""
        i = self.instance.repository_invitations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/repository_invitations'),
            params={'per_page': 100},
            headers={}
        )

    def test_respositories(self):
        """
        Show that an authenticated user can iterate over their repositories.
        """
        i = self.instance.repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/repos'),
            params={'per_page': 100},
            headers={}
        )

    def test_respositories_accepts_params(self):
        """Show that an #repositories accepts params."""
        i = self.instance.repositories(type='all',
                                       direction='desc',
                                       sort='created')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/repos'),
            params={'per_page': 100, 'type': 'all', 'direction': 'desc',
                    'sort': 'created'},
            headers={}
        )

    def test_issues_on(self):
        """Show that a user can iterate over a repository's issues."""
        i = self.instance.issues_on('owner', 'repo')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repos/owner/repo/issues'),
            params={'per_page': 100},
            headers={}
        )

    def test_issues_on_with_params(self):
        """Show that #issues_on accepts multiple parameters."""
        params = {'milestone': 1, 'state': 'all', 'assignee': 'owner',
                  'mentioned': 'someone', 'labels': 'bug,high'}
        i = self.instance.issues_on('owner', 'repo', **params)
        self.get_next(i)

        params.update(per_page=100)

        self.session.get.assert_called_once_with(
            url_for('repos/owner/repo/issues'),
            params=params,
            headers={}
        )

    def test_starred(self):
        """
        Show that one can iterate over an authenticated user's stars.
        """
        i = self.instance.starred()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/starred'),
            params={'per_page': 100},
            headers={}
        )

    def test_starred_by(self):
        """Show that one can iterate over a user's stars."""
        i = self.instance.starred_by('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/starred'),
            params={'per_page': 100},
            headers={}
        )

    def test_subscriptions(self):
        """
        Show that one can iterate over an authenticated user's subscriptions.
        """
        i = self.instance.subscriptions()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/subscriptions'),
            params={'per_page': 100},
            headers={}
        )

    def test_subscriptions_for(self):
        """Show that one can iterate over a user's subscriptions."""
        i = self.instance.subscriptions_for('sigmavirus24')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/subscriptions'),
            params={'per_page': 100},
            headers={}
        )

    def test_user_issues(self):
        """Test that one can iterate over a user's issues."""
        i = self.instance.user_issues()
        # Get the next item from the iterator
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/issues'),
            params={'per_page': 100},
            headers={}
        )

    def test_user_issues_with_parameters(self):
        """Test that one may pass parameters to GitHub#user_issues."""
        # Set up the parameters to be sent
        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z', 'per_page': 25}

        # Make the call with the paramters
        i = self.instance.user_issues(**params)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('user/issues'),
            params=params,
            headers={}
        )

    def test_repositories_by(self):
        """Test that one can iterate over a user's repositories."""
        i = self.instance.repositories_by('sigmavirus24')

        # Get the next item from the iterator
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/repos'),
            params={'per_page': 100},
            headers={}
        )

    def test_repositories_by_with_type(self):
        """
        Test that one can iterate over a user's repositories with a type.
        """
        i = self.instance.repositories_by('sigmavirus24', 'all')

        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/repos'),
            params={'per_page': 100, 'type': 'all'},
            headers={}
        )


class TestGitHubSearchIterators(helper.UnitSearchIteratorHelper):

    """Test GitHub methods that return search iterators."""

    described_class = GitHub
    example_data = None

    def test_search_code(self):
        """Verify the request to search for code."""
        i = self.instance.search_code(
            'addClass in:file language:js repo:jquery/jquery')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('search/code'),
            params={'per_page': 100,
                    'q': 'addClass in:file language:js repo:jquery/jquery'},
            headers={}
        )

    def test_search_commits(self):
        """Verify the request to search for commits."""
        i = self.instance.search_commits(
            'css repo:octocat/Spoon-Knife')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('search/commits'),
            params={'per_page': 100,
                    'q': 'css repo:octocat/Spoon-Knife'},
            headers={'Accept': 'application/vnd.github.cloak-preview'}
        )

    def test_search_issues(self):
        """Verify the request to search for issues."""
        i = self.instance.search_issues(
            'windows label:bug language:python state:open',
            sort='created', order='asc')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('search/issues'),
            params={'order': 'asc',
                    'per_page': 100,
                    'q': 'windows label:bug language:python state:open',
                    'sort': 'created'},
            headers={}
        )

    def test_search_repositories(self):
        """Verify the request to search for repositories."""
        i = self.instance.search_repositories(
            'tetris language:assembly',
            sort='stars', order='asc')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('search/repositories'),
            params={'order': 'asc',
                    'per_page': 100,
                    'q': 'tetris language:assembly',
                    'sort': 'stars'},
            headers={}
        )

    def test_search_users(self):
        """Verify the request to search for users."""
        i = self.instance.search_users(
            'tom repos:>42 followers:>1000')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('search/users'),
            params={'per_page': 100,
                    'q': 'tom repos:>42 followers:>1000'},
            headers={}
        )


class TestGitHubRequiresAuthentication(
        helper.UnitRequiresAuthenticationHelper):

    """Test methods that require authentication."""

    described_class = GitHub
    example_data = None

    def test_activate_membership(self):
        """Verify that activating a membership requires authentication."""
        self.assert_requires_auth(self.instance.activate_membership)

    def test_add_email_addresses(self):
        """Verify a user must be authenticated to add email addresses."""
        self.assert_requires_auth(self.instance.add_email_addresses, [])

    def test_authorization(self):
        """A user must be authenticated to retrieve an authorization."""
        self.assert_requires_auth(self.instance.authorization, 1)

    def test_authorizations(self):
        """Show that one needs to authenticate to use #authorizations."""
        self.assert_requires_auth(self.instance.authorizations)

    def test_create_gpg_key(self):
        """Show that GitHub#create_gpg_key requires auth."""
        self.assert_requires_auth(self.instance.create_gpg_key)

    def test_create_issue(self):
        """Show that GitHub#create_issue requires auth."""
        self.assert_requires_auth(self.instance.create_issue,
                                  'owner', 'repo', 'title')

    def test_create_key(self):
        """Show that GitHub#create_key requires auth."""
        self.assert_requires_auth(self.instance.create_key, 'title', 'key')

    def test_create_repository(self):
        """Show that GitHub#create_repository requires auth."""
        self.assert_requires_auth(self.instance.create_repository, 'repo')

    def test_delete_email_addresses(self):
        """Verify a user must be authenticated to delete email addresses."""
        self.assert_requires_auth(self.instance.delete_email_addresses, [])

    def test_emails(self):
        """Show that one needs to authenticate to use #emails."""
        self.assert_requires_auth(self.instance.emails)

    def test_feeds(self):
        """Show that one needs to authenticate to use #feeds."""
        self.assert_requires_auth(self.instance.feeds)

    def test_follow(self):
        """Show that one needs to authenticate to use #follow."""
        self.assert_requires_auth(self.instance.follow, 'foo')

    def test_gists(self):
        """Show that one needs to authenticate to use #gists."""
        self.assert_requires_auth(self.instance.gists)

    def test_is_following(self):
        """Show that GitHub#is_following requires authentication."""
        self.assert_requires_auth(self.instance.is_following, 'foo')

    def test_is_starred(self):
        """Show that GitHub#is_starred requires authentication."""
        self.assert_requires_auth(self.instance.is_starred, 'foo', 'bar')

    def test_issues(self):
        """Show that one needs to authenticate to use #issues."""
        self.assert_requires_auth(self.instance.issues)

    def test_key(self):
        """Show that retrieving user key requires authentication."""
        self.assert_requires_auth(self.instance.key, 1)

    def test_keys(self):
        """Show that one needs to authenticate to use #keys."""
        self.assert_requires_auth(self.instance.keys)

    def test_me(self):
        """Show that GitHub#me requires authentication."""
        self.assert_requires_auth(self.instance.me)

    def test_notifications(self):
        """Show that one needs to authenticate to use #gists."""
        self.assert_requires_auth(self.instance.notifications)

    def test_organization_issues(self):
        """Show that one needs to authenticate to use #organization_issues."""
        self.assert_requires_auth(self.instance.organization_issues, 'org')

    def test_organizations(self):
        """Show that one needs to authenticate to use #organizations."""
        self.assert_requires_auth(self.instance.organizations)

    def test_pubsubhubbub(self):
        """Show that one needs to authenticate to use pull request."""
        self.assert_requires_auth(self.instance.pubsubhubbub,
                                  mode='', topic='', callback='')

    def test_repositories(self):
        """Show that one needs to authenticate to use #repositories."""
        self.assert_requires_auth(self.instance.repositories)

    def test_repository_invitations(self):
        """Show that getting the repo invitations requires authentication."""
        self.assert_requires_auth(self.instance.repository_invitations)

    def test_star(self):
        """Show that starring a repository requires authentication."""
        self.assert_requires_auth(self.instance.star, username='', repo='')

    def test_starred(self):
        """Show that one needs to authenticate to use #starred."""
        self.assert_requires_auth(self.instance.starred)

    def test_unfollow(self):
        """Show that unfollowing a user requires authentication."""
        self.assert_requires_auth(self.instance.unfollow, 'foo')

    def test_unstar(self):
        """Show that unstarring requires authentication."""
        self.assert_requires_auth(self.instance.unstar, username='', repo='')

    def test_user_issues(self):
        """Show that GitHub#user_issues requires authentication."""
        self.assert_requires_auth(self.instance.user_issues)


class TestGitHubAuthorizations(helper.UnitHelper):
    described_class = GitHub
    example_data = None

    def create_session_mock(self, *args):
        session = super(TestGitHubAuthorizations,
                        self).create_session_mock(*args)
        session.retrieve_client_credentials.return_value = ('id', 'secret')
        return session

    def test_revoke_authorization(self):
        """Test that GitHub#revoke_authorization calls the expected methods.

        It should use the session's delete and temporary_basic_auth methods.
        """
        self.instance.revoke_authorization('access_token')
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/id/tokens/access_token',
            params={'client_id': None, 'client_secret': None}
        )
        self.session.temporary_basic_auth.assert_called_once_with(
            'id', 'secret'
        )

    def test_revoke_authorizations(self):
        """Test that GitHub#revoke_authorizations calls the expected methods.

        It should use the session's delete and temporary_basic_auth methods.
        """
        self.instance.revoke_authorizations()
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/id/tokens',
            params={'client_id': None, 'client_secret': None}
        )
        self.session.temporary_basic_auth.assert_called_once_with(
            'id', 'secret'
        )


class TestGitHubEnterprise(helper.UnitGitHubEnterpriseHelper):

    described_class = GitHubEnterprise

    def test_admin_stats(self):
        """Verify the request for checking admin stats."""
        self.instance.admin_stats(option='all')
        self.session.get.assert_called_once_with(
            enterprise_url_for('enterprise/stats/all')
        )

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance) == '<GitHub Enterprise [{0}]>'.format(
            enterprise_url_for()
        )


class TestGitHubStatus(helper.UnitHelper):

    """Test methods on GitHubStatus."""

    described_class = GitHubStatus

    def test_api(self):
        """Verify the request for /api."""
        with helper.mock.patch.object(GitHubStatus, '_recipe') as _recipe:
            self.instance.api()
            _recipe.assert_called_once_with('api.json')

    def test_last_message(self):
        """Verify the request for /api/last-message."""
        with helper.mock.patch.object(GitHubStatus, '_recipe') as _recipe:
            self.instance.last_message()
            _recipe.assert_called_once_with('api', 'last-message.json')

    def test_messages(self):
        """Verify the request for /api/messages."""
        with helper.mock.patch.object(GitHubStatus, '_recipe') as _recipe:
            self.instance.messages()
            _recipe.assert_called_once_with('api', 'messages.json')

    def test_status(self):
        """Verify the request for /api/status."""
        with helper.mock.patch.object(GitHubStatus, '_recipe') as _recipe:
            self.instance.status()
            _recipe.assert_called_once_with('api', 'status.json')
