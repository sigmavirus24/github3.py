#!/usr/bin/env python

import os
import json
import getpass
import requests

try:
    prompt = raw_input
except NameError:
    # python3
    prompt = input

user = ''
while not user:
    user = prompt('Username: ').strip()

passwd = ''
while not passwd:
    passwd = getpass.getpass('Password: ')

s = requests.Session()
s.auth = (user, passwd)

for file_name in os.listdir('.'):
    if file_name.startswith('legacy_') or (file_name == 'archive'):
        continue

    json_data = {}
    with open(file_name, 'rb') as f:
        json_data = json.load(f)

    url = json_data.get('url')
    if url:
        if file_name in ('branch', 'commit'):
            continue
        url = handle(file_name, json_data)

    print("{0}: {1}".format(file_name, json_data['url']))
    response = s.get(json_data['url'])
    with open(file_name, 'wb') as f:
        json.dump(response.json(), f)


def handle(name, json):
    if name == 'branch'
