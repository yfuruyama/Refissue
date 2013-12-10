# -*- coding: utf-8 -*-

import math


def document_similarity(doc1, doc2):
    return _cosine_similarity(doc1, doc2)


def _cosine_similarity(doc1, doc2):
    merged = doc1 + doc2
    unique = list(set(merged))

    c1 = []
    for index, d in enumerate(unique):
        c1.append(1 if d in doc1 else 0)
    c2 = []
    for index, d in enumerate(unique):
        c2.append(1 if d in doc2 else 0)

    denominator = math.sqrt(sum(c1)) * math.sqrt(sum(c2))
    numerator = sum(map(lambda x, y: x * y, c1, c2))

    if (denominator) == 0:
        return 0
    else:
        return float(numerator) / float(denominator)
