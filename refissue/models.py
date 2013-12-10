# -*- coding: utf-8 -*-

import logging
import os

from similarity import document_similarity
from igo.Tagger import Tagger


class Issue(object):
    def __init__(self, id, number, title, body):
        self.id = id
        self.number = number
        self.title = title
        self.body = body
        self.keywords = _analyzer.pickup_keywords(
            self.title + ' ' + self.body
            )

    @classmethod
    def from_dict(cls, issue_dict):
        id = issue_dict.get('id')
        number = issue_dict.get('number')
        title = issue_dict.get('title')
        body = issue_dict.get('body')
        return cls(id, number, title, body)

    def search_most_similar_issues(self, issues, n):
        # exclude self issue from issues
        issues = [issue for issue in issues if issue.id != self.id]
        results = [(self.compare(issue), issue) for issue in issues]
        results.sort(cmp=lambda a, b: cmp(a[0], b[0]))
        results.reverse()
        return results[0:n]

    def compare(self, other):
        return document_similarity(self.keywords, other.keywords)


class Morpheme(object):
    def __init__(self, surface, word_class, word_class_fine_1, original):
        self.surface = surface
        self.word_class = word_class
        self.word_class_fine_1 = word_class_fine_1
        self.original = original


class MorphemeAnalyzer(object):
    tagger = Tagger(
        os.path.join(os.path.dirname(__file__), 'ipadic-gae'),
        gae=True
        )

    def _analyze(self, doc):
        u""" 形態素解析を行う

        featureの中身:
        品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
        """
        morphemes = []
        for m in self.tagger.parse(doc):
            parts = m.feature.split(',')
            morphemes.append(
                Morpheme(m.surface, parts[0], parts[1], parts[6])
                )
        return morphemes

    def pickup_keywords(self, doc):
        u""" ドキュメントからキーワードのみ取り出す

        品詞が名詞, 動詞, 形容詞であり品詞細分類が非自立以外の形態素を抽出
        """
        morphemes = self._analyze(doc)
        keywords = []
        for m in morphemes:
            if m.word_class in (u'名詞', u'動詞'):
                if m.word_class_fine_1 == u'非自立':
                    continue
            elif not m.word_class in (u'形容詞'):
                continue
            keyword = m.original if m.original != '*' else m.surface
            keywords.append(keyword)
        return keywords


_analyzer = MorphemeAnalyzer()
