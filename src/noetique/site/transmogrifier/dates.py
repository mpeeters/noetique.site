# -*- coding: utf-8 -*-

from DateTime import DateTime
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import classProvides
from zope.interface import implements


def is_not_empty(value):
    if value == 'None':
        return False
    return bool(value)


class DatesCorrector(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.creationkey = 'creation_date'
        self.modificationkey = 'modification_date'
        self.effectivekey = 'effectiveDate'
        self.expirationkey = 'expirationDate'

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey:
                yield item
                continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:
                yield item
                continue

            creationdate = item.get(self.creationkey, None)
            if is_not_empty(creationdate) and hasattr(obj, 'creation_date'):
                obj.creation_date = DateTime(creationdate)

            modificationdate = item.get(self.modificationkey, None)
            if is_not_empty(modificationdate) and hasattr(obj, 'modification_date'):
                obj.modification_date = DateTime(modificationdate)

            effectivedate = item.get(self.effectivekey, None)
            if is_not_empty(effectivedate) and hasattr(obj, 'effective_date'):
                obj.effective_date = DateTime(effectivedate)

            expirationdate = item.get(self.expirationkey, None)
            if is_not_empty(expirationdate) and hasattr(obj, 'expiration_date'):
                obj.expiration_date = DateTime(expirationdate)

            obj.indexObject()
            yield item
