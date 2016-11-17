# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from zope.interface import classProvides
from zope.interface import implements

TO_IGNORE = [
    'bookOrder',
    'bookAfterward',
    'authorPicture',
    'authorIntroduction',
    'backerName',
    'backerPicture',
    'backerIntroduction',
    'bookComment',
    'bookSummary',
    'bookFourthCover',
]

TO_CHANGE = {
    'publisherName': 'publisher',
    'bookCollection': 'collection',
    'bookType': 'kind',
    'bookLanguage': 'langue',
    'pageNumber': 'pages',
    'bookFormat': 'format',
    'publicationYear': 'year',
    'bookISBN': 'isbn',
    'bookAudience': 'audience',
    'bookCover': 'cover',
    'bookForeword': 'foreword',
    'authorName': 'author',
}


class BookTypeChanger(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            portal_type = item.get('_type', '')
            if portal_type == 'NoetiqueBook':
                item['_type'] = 'noetique.site.Book'
            yield item


class BookFieldsManipulator(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            portal_type = item.get('_type', '')
            if portal_type != 'noetique.site.Book':
                yield item
                continue

            # Merge bookComment & description in description
            bookComment = item.get('bookComment', '')
            description = item.get('description', '')
            item['description'] = '\n'.join([bookComment, description])

            # Merge bookSummary & bookFourthCover in summary
            bookSummary = item.get('bookSummary', '')
            bookFourthCover = item.get('bookFourthCover', '')
            item['summary'] = '<br/><br/>'.join([bookSummary, bookFourthCover])

            for attr in TO_IGNORE:
                if attr in item:
                    item.pop(attr)

            for old_attr, new_attr in TO_CHANGE.items():
                if not old_attr in item:
                    continue
                value = item.get(old_attr)
                item.pop(old_attr)
                item[new_attr] = value

            yield item


class BookFormatFixer(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            portal_type = item.get('_type', '')
            if portal_type != 'noetique.site.Book':
                yield item
                continue

            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey:
                yield item
                continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:
                yield item
                continue

            obj.format = item['format']
            obj.indexObject()
            yield item
