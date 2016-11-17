# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import classProvides
from zope.interface import implements
import json


class JSONFixer(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.fileskey = defaultMatcher(options, 'files-key', name, 'files')
        self.key = options.get('key', 'content').strip()

    def __iter__(self):
        for item in self.previous:
            fileskey = self.fileskey(*item.keys())[0]

            files = item.get(fileskey)
            if not files:
                yield item
                continue

            content = files.get(self.key)
            if not content:
                yield item
                continue

            data = json.loads(content['data'])
            if isinstance(data, list):
                data = data[0]
            new_data = json.dumps(data)
            new_data = new_data.replace('localhost:8080/noetique/plone/',
                                        'localhost:8080/plone/')
            new_data = new_data.replace('/noetique/plone/', '')
            item[fileskey][self.key]['data'] = new_data
            yield item
