#!/usr/bin/env python

import os
import json
import getpass
import requests

IGNORE = (
    'archive',
    'authorization',
    'branch',
    'code_frequency',
    'commit',
    'commit_activity',
    'contributor_statistics',
    'create_content',
    'emails',
    'event',
    'language',
    'legacy_email',
    'legacy_issue',
    'legacy_repo',
    'legacy_user',
    'merge',
    'meta',
    'pull_file',
    'ratelimit',
    'tag',
    'template',
    'templates',
    'weekly_commit_count',
)

try:
    prompt = raw_input
except NameError:
    # python3
    prompt = input


def handle(file_name, json_data):
    if file_name == 'status' and isinstance(json_data, list):
        json_data = json_data[0]

    with open(file_name, 'wb') as f:
        json.dump(json_data, f)


def get_auth():
    user = ''
    while not user:
        user = prompt('Username: ').strip()

    passwd = ''
    while not passwd:
        passwd = getpass.getpass('Password: ')

    return user, passwd


def main():
    auth = get_auth()
    s = requests.Session()
    s.auth = auth

    for file_name in sorted(os.listdir('.')):
        if file_name in IGNORE or file_name.endswith('.py'):
            continue

        json_data = {}
        with open(file_name, 'rb') as f:
            try:
                json_data = json.load(f)
            except ValueError:
                print("Couldn't process: {0}".format(file_name))

        url = json_data.get('url')

        print("{0}: {1}".format(file_name, url))

        if not url:
            print("Skipping {0}".format(file_name))
            continue

        response = s.get(url)
        if response.status_code == 200:
            handle(file_name, response.json())
