# -*- coding: utf-8 -*-
"""
github3.licenses
================

This module contains the classes relating to licenses

See also: https://developer.github.com/v3/licenses/
"""
from __future__ import unicode_literals

from .models import GitHubCore


class License(GitHubCore):

    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.drax-preview+json'
    }

    def _update_attributes(self, license):
        # name of license
        self.name = license.get('name')

        # permission of license
        self.permitted = license.get('permitted')

        # category of license
        self.category = license.get('category')

        # forbidden
        self.forbidden = license.get('forbidden')

        # featured
        self.featured = license.get('featured')

        # html url
        self.html_url = license.get('html_url')

        # body
        self.body = license.get('body')

        # key
        self.key = license.get('key')

        # description
        self.description = license.get('description')

        # implementation
        self.implementation = license.get('implementation')

        # required
        self.required = license.get('required')

    def _repr(self):
        return '<License [{0}]>'.format(self.name)
