# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from z3c.relationfield.relation import create_relation
from zope.interface import classProvides
from zope.interface import implements

REFERENCE_QUEUE = []
MATCHING_UIDS = {}


class ReferencesImporter(object):
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
            refs = item.get('relatedItems', [])
            if refs:
                REFERENCE_QUEUE.append(path)
            uid = item.get('_uid', "")
            if uid:
                MATCHING_UIDS[uid] = path
            yield item

        print REFERENCE_QUEUE
        for path in REFERENCE_QUEUE:
            obj = self.context.unrestrictedTraverse(str(path), None)
            if obj is None:
                continue

            relatedItems = obj.relatedItems
            obj.relatedItems = []
            for uid in relatedItems:
                if not uid in MATCHING_UIDS:
                    continue
                dest_path = MATCHING_UIDS[uid]
                dest_path = str('/plone/%s' % dest_path)
                relation = create_relation(dest_path)
                obj.relatedItems.append(relation)
