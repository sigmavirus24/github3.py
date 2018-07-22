import base64
import betamax
import os
import pytest

from betamax_matchers import json_body

credentials = [os.environ.get('GH_USER', 'foo').encode(),
               os.environ.get('GH_PASSWORD', 'bar').encode()]

betamax.Betamax.register_request_matcher(json_body.JSONBodyMatcher)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'

    record_mode = os.environ.get('GH_RECORD_MODE', 'once')

    config.default_cassette_options['record_mode'] = record_mode

    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'x' * 20)
        )

    config.default_cassette_options['match_requests_on'].append('json-body')

    config.define_cassette_placeholder(
        '<BASIC_AUTH>',
        base64.b64encode(b':'.join(credentials)).decode()
        )


@pytest.fixture
def betamax_simple_body(request):
    """Return configuration to match cassette on uri, method and body."""
    request.cls.betamax_simple_body = {
        'match_requests_on': ['uri', 'method', 'body']
    }


@pytest.fixture
def enterprise_url(request):
    """Configure class with enterprise url."""
    request.cls.enterprise_url = 'https://enterprise.github3.com'


class IfNoneMatchMatcher(betamax.BaseMatcher):

    name = 'if-none-match'

    def match(self, request, recorded_request):
        request_header  = request.headers.get('If-None-Match')
        recorded_header = recorded_request['headers'].get('If-None-Match')
        matches = True if request_header == recorded_header else False
        return matches


betamax.Betamax.register_request_matcher(IfNoneMatchMatcher)
