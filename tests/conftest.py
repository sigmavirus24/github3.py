import base64
import betamax
import os

from betamax_matchers import json_body
from betamax_serializers import pretty_json

credentials = [os.environ.get('GH_USER', 'foo').encode(),
               os.environ.get('GH_PASSWORD', 'bar').encode()]

betamax.Betamax.register_request_matcher(json_body.JSONBodyMatcher)
betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'

    record_mode = 'never' if os.environ.get('TRAVIS_GH3') else 'once'

    config.default_cassette_options['record_mode'] = record_mode
    config.default_cassette_options['serialize_with'] = 'prettyjson'

    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'x' * 20)
        )

    config.define_cassette_placeholder(
        '<BASIC_AUTH>',
        base64.b64encode(b':'.join(credentials)).decode()
        )
