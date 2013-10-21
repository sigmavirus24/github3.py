import base64
import betamax
import os

credentials = [os.environ.get('GH_USER', 'foo'),
               os.environ.get('GH_PASSWORD', 'bar')]

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'
    record_mode = 'once'
    if os.environ.get('TRAVIS_GH3'):
        record_mode = 'never'
    config.default_cassette_options['record_mode'] = record_mode

    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'x' * 20)
        )

    config.define_cassette_placeholder(
        '<BASIC_AUTH>',
        base64.b64encode(':'.join(credentials))
        )
