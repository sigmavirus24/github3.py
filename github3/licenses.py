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
        self._api = self._get_attribute(license, 'url')
        self.name = self._get_attribute(license, 'name')
        self.permitted = self._get_attribute(license, 'permitted')
        self.category = self._get_attribute(license, 'category')
        self.forbidden = self._get_attribute(license, 'forbidden')
        self.featured = self._get_attribute(license, 'featured')
        self.html_url = self._get_attribute(license, 'html_url')
        self.body = self._get_attribute(license, 'body')
        self.key = self._get_attribute(license, 'key')
        self.description = self._get_attribute(license, 'description')
        self.implementation = self._get_attribute(license, 'implementation')
        self.required = self._get_attribute(license, 'required')

    def _repr(self):
        return '<License [{0}]>'.format(self.name)
