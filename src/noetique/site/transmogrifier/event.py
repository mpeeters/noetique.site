# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from dateutil import parser
from zope.interface import classProvides
from zope.interface import implements
import pytz


class EventImporter(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        tz = pytz.timezone('Europe/Brussels')
        for item in self.previous:
            portal_type = item.get('_type', '')
            if portal_type != 'Event':
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

            if not 'startDate' in item:
                yield item
                continue

            start_date = item['startDate']
            start_date = start_date.replace('Universal', 'GMT')
            start_date = parser.parse(start_date).replace(tzinfo=None)
            obj.start = tz.localize(start_date)
            end_date = item['endDate']
            end_date = end_date.replace('Universal', 'GMT')
            end_date = parser.parse(end_date).replace(tzinfo=None)
            obj.end = tz.localize(end_date)
            obj.contact_email = item['contactEmail']
            obj.contact_name = item['contactName']
            obj.contact_phone = item['contactPhone']
            obj.event_url = item['eventUrl']
            yield item
