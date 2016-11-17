# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import classProvides
from zope.interface import implements


class WorkflowConverter(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

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

            yield item
