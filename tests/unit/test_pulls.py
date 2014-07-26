"""Unit tests for the github3.pulls module."""
import json
import os

from .helper import UnitHelper, UnitIteratorHelper

from github3.pulls import PullRequest


def get_pr_example_data():
    """Load the example data for the PullRequest object."""
    directory = os.path.dirname(__file__)
    example = os.path.join(directory, 'pull_request_example')
    with open(example) as fd:
        data = json.load(fd)
    return data


class TestPullRequest(UnitHelper):

    """PullRequest unit tests."""

    described_class = PullRequest
    example_data = get_pr_example_data()


class TestPullRequestIterator(UnitIteratorHelper):

    """Test PullRequest methods that return Iterators."""

    pass
