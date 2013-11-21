import requests

from github3 import __version__


class GitHubSession(requests.Session):
    def __init__(self):
        super(GitHubSession, self).__init__()
        self.headers.update({
            # Only accept JSON responses
            'Accept': 'application/vnd.github.v3.full+json',
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always sending JSON
            'Content-Type': "application/json",
            # Set our own custom User-Agent string
            'User-Agent': 'github3.py/{0}'.format(__version__),
            })

    def basic_auth(self, username, password):
        """Set the Basic Auth credentials on this Session.

        :param str username: Your GitHub username
        :param str password: Your GitHub password
        """
        if not (username and password):
            return

        self.auth = (username, password)

    def token_auth(self, token):
        """Use an application token for authentication.

        :param str token: Application token retrieved from GitHub's
            /authorizations endpoint
        """
        if not token:
            return

        self.headers.update({
            'Authorization': 'token {0}'.format(token)
            })

    def oauth2_auth(self, client_id, client_secret):
        """Use OAuth2 for authentication.

        It is suggested you install requests-oauthlib to use this.

        :param str client_id: Client ID retrieved from GitHub
        :param str client_secret: Client secret retrieved from GitHub
        """
        raise NotImplementedError('These features are not implemented yet')
