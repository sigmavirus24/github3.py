import betamax
import os

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'
    record_mode = 'once'
    if os.environ.get('TRAVIS_GH3'):
        record_mode = 'never'
    config.default_cassette_options['record_mode'] = record_mode

    config.define_cassette_placeholder(
        '<AUTH_TOKEN>',
        os.environ.get('GH_AUTH', 'xxxxxxxxxxx')
        )
