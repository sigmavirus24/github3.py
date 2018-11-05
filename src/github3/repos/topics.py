# -*- coding: utf-8 -*-
"""Topics related logic."""
from __future__ import unicode_literals

from .. import models


class Topics(models.GitHubCore):
    """Representation of the repository topics.

    .. attribute:: names

        The names of the topics.
    """

    def _update_attributes(self, topics):
        self.names = topics["names"]

    def _repr(self):
        return "<Topics [{0}]>".format(", ".join(self.names))
