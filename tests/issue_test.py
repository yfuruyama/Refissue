# -*- coding: utf-8 -*-

import pytest

from refissue.issue import Issue
from mock import Mock, patch
from contextlib import nested


class TestIssue(object):
    def setup_method(self, method):
        with patch('refissue.issue._analyzer.pickup_keywords', return_value=''):
            self.issue = Issue(1, 1, 'mytitle', 'mybody')

    def test_search_most_similar_issues(self):
        def _compare(other):
            return other.similarity
        with patch('refissue.issue.Issue.compare', side_effect=_compare):
            other_issues = [
                Mock(id=2, similarity=0.7),
                Mock(id=3, similarity=0.4)
                ]
            results = self.issue.search_most_similar_issues(other_issues, 1)
            result = results[0]
            assert type(result) is tuple and result[0] == 0.7

            other_issues = []
            results = self.issue.search_most_similar_issues(other_issues, 1)
            assert type(results) is list and len(results) == 0
