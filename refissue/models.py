# -*- coding: utf-8 -*-

import logging
import os

from similarity import document_similarity
from igo.Tagger import Tagger


_igo_dictionary = os.path.join(os.path.dirname(__file__), 'ipadic-gae')


class Issue(object):
    def __init__(self, id, number, title, body):
        self.id = id
        self.number = number
        self.title = title
        self.body = body
        self.morpheme = self._morpheme_analyze()

    @classmethod
    def from_dict(cls, issue_dict):
        id = issue_dict.get('id')
        number = issue_dict.get('number')
        title = issue_dict.get('title')
        body = issue_dict.get('body')
        return cls(id, number, title, body)

    def _morpheme_analyze(self):
        u"""
        品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
        """
        effective_morpheme = []
        logging.info('------------------------------')
        logging.info(self.body)
        for m in Tagger(_igo_dictionary, gae=True).parse(self.body):
            # logging.info(m.feature)
            word_class, word_class_fine_1 = m.feature.split(',')[0:2]
            if word_class in (u'名詞', u'動詞'):
                if word_class_fine_1 == u'非自立':
                    continue
            # elif not word_class in (u'形容詞', u'助動詞'):
            elif not word_class in (u'形容詞'):
                continue
            original = m.feature.split(',')[6]
            keyword = original if original != '*' else m.surface
            logging.info(keyword)
            effective_morpheme.append(keyword)
        return effective_morpheme

    def search_most_similar_issues(self, issues, n):
        issues = [issue for issue in issues if issue.id != self.id]
        similarities = [(self.compare(issue), issue) for issue in issues]
        similarities.sort(cmp=lambda a, b: cmp(a[0], b[0]))
        similarities.reverse()
        return similarities[0:n]

    def compare(self, other):
        return document_similarity(self.morpheme, other.morpheme)
