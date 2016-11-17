# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import classProvides
from zope.interface import implements


class PathReducer(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey:
                yield item
                continue
            path = item[pathkey]
            path = path.replace('/noetique/plone/', '')
            # Unicode paths cannot be traversed to
            path = path.encode().lstrip('/')
            item[pathkey] = path
            yield item


class PathExpander(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            if not pathkey:
                yield item
                continue
            path = item[pathkey]
            if path.startswith('/'):
                path = '/noetique/plone%s' % path
            else:
                path = '/noetique/plone/%s' % path
            item[pathkey] = path
            yield item
