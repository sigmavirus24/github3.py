from github3.repos.repo import Repository

from .helper import UnitHelper


class TestRepository(UnitHelper):
    described_class = Repository
    example_data = {
        "id": 1296269,
        "owner": {
            "login": "octocat",
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat"
            },
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "This your first repo!",
        "private": False,
        "fork": False,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "git_url": "git://github.com/octocat/Hello-World.git",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "mirror_url": "git://git.example.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": None,
        "forks": 9,
        "forks_count": 9,
        "watchers": 80,
        "watchers_count": 80,
        "size": 108,
        "master_branch": "master",
        "open_issues": 0,
        "open_issues_count": 0,
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "organization": {
            "login": "octocat",
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat",
            "type": "Organization"
            },
        "parent": {
            "id": 1296269,
            "owner": {
                "login": "octocat",
                "id": 1,
                "avatar_url": "https://github.com/images/error/octocat.gif",
                "gravatar_id": "somehexcode",
                "url": "https://api.github.com/users/octocat"
                },
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "description": "This your first repo!",
            "private": False,
            "fork": True,
            "url": "https://api.github.com/repos/octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "clone_url": "https://github.com/octocat/Hello-World.git",
            "git_url": "git://github.com/octocat/Hello-World.git",
            "ssh_url": "git@github.com:octocat/Hello-World.git",
            "svn_url": "https://svn.github.com/octocat/Hello-World",
            "mirror_url": "git://git.example.com/octocat/Hello-World",
            "homepage": "https://github.com",
            "language": None,
            "forks": 9,
            "forks_count": 9,
            "watchers": 80,
            "watchers_count": 80,
            "size": 108,
            "master_branch": "master",
            "open_issues": 0,
            "open_issues_count": 0,
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z"
            },
        "source": {
            "id": 1296269,
            "owner": {
                "login": "octocat",
                "id": 1,
                "avatar_url": "https://github.com/images/error/octocat.gif",
                "gravatar_id": "somehexcode",
                "url": "https://api.github.com/users/octocat"
                },
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "description": "This your first repo!",
            "private": False,
            "fork": True,
            "url": "https://api.github.com/repos/octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "clone_url": "https://github.com/octocat/Hello-World.git",
            "git_url": "git://github.com/octocat/Hello-World.git",
            "ssh_url": "git@github.com:octocat/Hello-World.git",
            "svn_url": "https://svn.github.com/octocat/Hello-World",
            "mirror_url": "git://git.example.com/octocat/Hello-World",
            "homepage": "https://github.com",
            "language": None,
            "forks": 9,
            "forks_count": 9,
            "watchers": 80,
            "watchers_count": 80,
            "size": 108,
            "master_branch": "master",
            "open_issues": 0,
            "open_issues_count": 0,
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z"
            },
        "has_issues": True,
        "has_wiki": True,
        "has_downloads": True
    }

    def test_asset(self):
        """Test retrieving an asset uses the right headers

        The Releases section of the API is still in Beta and uses custom
        headers
        """
        assert self.instance.asset(0) is None
        assert self.session.get.call_count == 0

        self.instance.asset(1)
        url = self.example_data['url'] + '/releases/assets/1'
        self.session.get.assert_called_once_with(
            url, headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_latest_pages_build(self):
        """Test retrieving the most recent pages build."""
        url = self.example_data['url'] + '/pages/builds/latest'
        self.instance.latest_pages_build()
        self.session.get.assert_called_once_with(url)

    def test_pages(self):
        """Test retrieving information about a repository's page."""
        url = self.example_data['url'] + '/pages'
        self.instance.pages()
        self.session.get.assert_called_once_with(url)
