# -*- coding: utf-8 -*-

import pytest

from refissue.similarity import document_similarity

_fixtures_morpheme = [
    ([u'スクリプト', u'デバッグ'], [u'デバッグ', u'スクリプト']),
    ([u'動作', u'検証', u'する'], [u'動作', u'検査']),
    ([], [u'動作', u'検査']),
    ([u'動作', u'検証', u'する'], []),
]


class TestSimilarity(object):
    @pytest.mark.parametrize(('doc1', 'doc2'), _fixtures_morpheme)
    def test_document_similarity(self, doc1, doc2):
        result = document_similarity(doc1, doc2)
        if set(doc1) == set(doc2):
            assert result >= 0.9999  # 誤差があるので
        elif set(doc1) is None or set(doc2) is None:
            assert result == 0
        else:
            assert 0 <= result <= 1
