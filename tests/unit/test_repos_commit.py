"""Unit tests for Repository Commits."""
import github3

from . import helper

example_commit_data = {
    "url": ("https://api.github.com/repos/octocat/Hello-World/commits/"
            "6dcb09b5b57875f334f61aebed695e2e4193db5e"),
    "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
    "html_url": ("https://github.com/octocat/Hello-World/commit/"
                 "6dcb09b5b57875f334f61aebed695e2e4193db5e"),
    "comments_url": ("https://api.github.com/repos/octocat/Hello-World/commits"
                     "/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments"),
    "commit": {
        "url": ("https://api.github.com/repos/octocat/Hello-World/git/commits/"
                "6dcb09b5b57875f334f61aebed695e2e4193db5e"),
        "author": {
            "name": "Monalisa Octocat",
            "email": "support@github.com",
            "date": "2011-04-14T16:00:49Z"
            },
        "committer": {
            "name": "Monalisa Octocat",
            "email": "support@github.com",
            "date": "2011-04-14T16:00:49Z"
            },
        "message": "Fix all the bugs",
        "tree": {
            "url": ("https://api.github.com/repos/octocat/Hello-World/tree/"
                    "6dcb09b5b57875f334f61aebed695e2e4193db5e"),
            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
            },
        "comment_count": 0
        },
    "author": {
        "login": "octocat",
        "id": 1,
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": ("https://api.github.com/users/octocat/"
                          "following{/other_user}"),
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": ("https://api.github.com/users/octocat/starred"
                        "{/owner}{/repo}"),
        "subscriptions_url": ("https://api.github.com/users/octocat/"
                              "subscriptions"),
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": ("https://api.github.com/users/octocat/"
                                "received_events"),
        "type": "User",
        "site_admin": False
        },
    "committer": {
        "login": "octocat",
        "id": 1,
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": ("https://api.github.com/users/octocat/following"
                          "{/other_user}"),
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": ("https://api.github.com/users/octocat/starred"
                        "{/owner}{/repo}"),
        "subscriptions_url": ("https://api.github.com/users/octocat/"
                              "subscriptions"),
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": ("https://api.github.com/users/octocat/"
                                "received_events"),
        "type": "User",
        "site_admin": False
        },
    "parents": [{
        "url": ("https://api.github.com/repos/octocat/Hello-World/commits/"
                "6dcb09b5b57875f334f61aebed695e2e4193db5e"),
        "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
    }],
    "stats": {
        "additions": 104,
        "deletions": 4,
        "total": 108
    },
    "files": [{
        "filename": "file1.txt",
        "additions": 10,
        "deletions": 2,
        "changes": 12,
        "status": "modified",
        "raw_url": ("https://github.com/octocat/Hello-World/raw/"
                    "7ca483543807a51b6079e54ac4cc392bc29ae284/file1.txt"),
        "blob_url": ("https://github.com/octocat/Hello-World/blob/"
                     "7ca483543807a51b6079e54ac4cc392bc29ae284/file1.txt"),
        "patch": "@@ -29,7 +29,7 @@\n....."
    }]
}

url_for = helper.create_url_helper(example_commit_data['url'])


class TestRepoCommitIterator(helper.UnitIteratorHelper):

    """Unit tests for RepoCommit iterator methods."""

    described_class = github3.repos.commit.RepoCommit
    example_data = example_commit_data

    def test_statuses(self):
        """Verify the request to iterate over statuses of a commit."""
        i = self.instance.statuses()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('statuses'),
            params={'per_page': 100},
            headers={}
        )

    def test_comments(self):
        """Verify the request to iterate over comments of a commit."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )
