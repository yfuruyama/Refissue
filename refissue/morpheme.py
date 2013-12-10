# -*- coding: utf-8 -*-

import os

from igo.Tagger import Tagger


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

    def __init__(self, dictionary_path):
        self.tagger = Tagger(dictionary_path, gae=True)
            # os.path.join(os.path.dirname(__file__), dictionary_path),
            # gae=True
            # )

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
