# -*- coding: utf-8 -*-

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocabulary_from_items(items):
    terms = [SimpleTerm(value=item[0], token=str(item[0]), title=item[1]) for item in items]
    return SimpleVocabulary(terms)
