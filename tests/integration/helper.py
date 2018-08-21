import copy
import datetime
import os
import unittest

import betamax
import dateutil.tz
import pytest

from betamax.cassette import cassette

import github3


@pytest.mark.usefixtures('betamax_simple_body')
class IntegrationHelper(unittest.TestCase):
    """Base test clas for integration tests."""

    def setUp(self):
        """Retrieve all of our environmen test variables."""
        self.user = os.environ.get('GH_USER', 'foo')
        self.password = os.environ.get('GH_PASSWORD', 'bar')
        self.token = os.environ.get('GH_AUTH', 'x' * 20)
        self.app_id = int(os.environ.get('GH_APP_ID', '0'))
        self.private_key_bytes = os.environ.get(
            'GH_APP_PRIVATE_KEY', u''
        ).encode('utf8')
        self.app_installation_id = int(
            os.environ.get('GH_APP_INSTALLATION_ID', '0')
        )
        self.gh = self.get_client()
        self.session = self.gh.session
        self.recorder = betamax.Betamax(self.session)

    def get_client(self):
        return github3.GitHub()

    def token_login(self):
        self.gh.login(token=self.token)

    def basic_login(self):
        self.gh.login(self.user, self.password)

    def app_bearer_login(self):
        """Login as a Github App."""
        if self.private_key_bytes and self.app_id:
            self.gh.login_as_app(self.private_key_bytes, self.app_id)
        else:
            token = 'x' * 20
            self.gh.session.app_bearer_token_auth(token, 600)

    def app_installation_login(self):
        """Login as the specific installation of a GitHub App."""
        if (self.current_cassette.is_recording() and
                self.private_key_bytes and
                self.app_id and
                self.installation_id):
            self.gh.login_as_app_installation(
                self.private_key_bytes, app_id=self.app_id,
                installation_id=self.app_installation_id,
                expire_in=30,
            )
            token = self.gh.session.auth
        else:
            token = 'v1.{}'.format('x' * 10)
            now = datetime.datetime.now(tz=dateutil.tz.UTC)
            expires_at_dt = now + datetime.timedelta(seconds=60*60)
            expires_at = expires_at_dt.isoformat()
            self.gh.session.app_installation_token_auth({
                'token': token,
                'expires_at': expires_at,
            })
        self.current_cassette.placeholders.append(
            cassette.Placeholder('<INSTALLATION_TOKEN>', token)
        )

    @property
    def current_cassette(self):
        """Short-cut to the recorder's current cassette."""
        return self.recorder.current_cassette

    def auto_login(self):
        """Log in appropriately based on discovered credentials"""

        if self.token:
            self.token_login()
        else:
            self.basic_login()

    def cassette_name(self, method, cls=None):
        class_name = cls or self.described_class
        return '_'.join([class_name, method])

    @property
    def described_class(self):
        class_name = self.__class__.__name__
        return class_name[4:]


class CustomHeadersMatcher(betamax.BaseMatcher):
    name = 'gh3-headers'

    def on_init(self):
        self.headers_matcher = betamax.matchers.HeadersMatcher()

    def match(self, request, recorded_request):
        request = request.copy()
        recorded_request = copy.deepcopy(recorded_request)
        request.headers.pop('User-Agent', None)
        recorded_request['headers'].pop('User-Agent', None)
        request.headers.pop('Accept-Encoding', None)
        recorded_request['headers'].pop('Accept-Encoding', None)
        request.headers.pop('Connection', None)
        recorded_request['headers'].pop('Connection', None)
        return self.headers_matcher.match(request, recorded_request)


betamax.Betamax.register_request_matcher(CustomHeadersMatcher)


@pytest.mark.usefixtures('enterprise_url')
class GitHubEnterpriseHelper(IntegrationHelper):

    def get_client(self):
        return github3.GitHubEnterprise(self.enterprise_url)


class GitHubStatusHelper(IntegrationHelper):

    def get_client(self):
        return github3.GitHubStatus()
