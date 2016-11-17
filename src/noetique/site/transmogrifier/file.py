# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from quintagroup.transmogrifier.binary import FileImporterSection as Base
from zope.interface import classProvides, implements


class FileImporter(Base):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            fileskey = self.fileskey(*item.keys())[0]

            if not (pathkey and fileskey):
                yield item
                continue
            if 'file-fields' not in item[fileskey]:
                yield item
                continue

            path = item[pathkey]
            obj = self.context.unrestrictedTraverse(path, None)
            if obj is None:
                yield item
                continue

            if IDexterityContent.providedBy(obj):
                manifest = item[fileskey]['file-fields']['data']
                for field, info in self.parseManifest(manifest).items():
                    fname = info['filename']
                    ct = info['mimetype']
                    data = item[fileskey][fname]['data']
                    if not self.condition(item, context=obj, fname=field,
                        filename=fname, data=data, mimetype=ct):
                        continue
                    if 'image' in field or 'cover' in field.lower():
                        if field == 'bookCover':
                            field = 'cover'
                        file = NamedBlobImage(data=data, contentType=ct)
                    else:
                        fname = fname.decode('utf-8')
                        file = NamedBlobFile(data=data, contentType=ct, filename=fname)
                    setattr(obj, field, file)
                    obj.reindexObject()

            yield item
