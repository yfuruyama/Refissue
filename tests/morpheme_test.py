# -*- coding: utf-8 -*-

import os
import pytest

from refissue.morpheme import MorphemeAnalyzer

_fixtures_morpheme = [
    (u'スクリプトのデバッグ', [u'スクリプト', u'デバッグ']),
    (u'動作検証しています', [u'動作', u'検証', u'する']),
]


class TestMorphemeAnalyzer(object):
    def setup_method(self, method):
        self.dictionary_path = os.path.join(
            os.path.dirname(__file__), '..', 'refissue', 'ipadic-gae'
            )

    def test_initialize(self):
        analyzer = MorphemeAnalyzer(self.dictionary_path)
        assert analyzer is not None

    @pytest.mark.parametrize(('doc', 'expected'), _fixtures_morpheme)
    def test_pickup_keywords(self, doc, expected):
        analyzer = MorphemeAnalyzer(self.dictionary_path)
        results = analyzer.pickup_keywords(doc)
        assert set(results) == set(expected)
