# -*- coding: utf-8 -*-

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel import model
from zope import schema
from zope.interface import implements


class IBook(model.Schema):
    """Book content type"""

    # fields
    title = schema.TextLine(
        title=u"Titre du livre",
        required=True
    )
    author = schema.TextLine(
        title=u"Auteur(s)",
        default=u"Marc Halévy",
        required=False,
    )
    description = schema.Text(
        title=u"Présentation du livre",
        required=True,
    )
    audience = schema.TextLine(
        title=u"Public",
        required=False,
    )
    cover = NamedBlobImage(
        title=u"Photo de couverture",
        required=False,
    )
    summary = RichText(
        title=u"Résumé détaillé du livre",
        required=False,
    )
    foreword = RichText(
        title=u"Préface du livre",
        required=False,
    )
    book = NamedBlobFile(
        title=u"Version gratuite du livre",
        required=False,
    )
    publisher = schema.TextLine(
        title=u"Editeur",
        required=False,
    )
    collection = schema.TextLine(
        title=u"Collection",
        required=False,
    )
    kind = schema.TextLine(
        title=u"Genre",
        required=False,
    )
    langue = schema.TextLine(
        title=u"Langue",
        required=False,
    )
    pages = schema.TextLine(
        title=u"Nombre de pages",
        required=False,
    )
    format = schema.TextLine(
        title=u"Format",
        required=False,
    )
    year = schema.TextLine(
        title=u"Année de publication",
        required=False,
    )
    isbn = schema.TextLine(
        title=u"ISBN",
        required=False,
    )

    # widgets
    directives.widget('description', rows=5)
    directives.widget('summary', rows=10)
    directives.widget('foreword', rows=10)

    # fieldsets
    model.fieldset(
        'metadata',
        label=u"Metadata",
        fields=['isbn', 'publisher', 'year', 'format', 'pages', 'collection', 'kind', 'langue']
    )


class Book(Item):
    implements(IBook)
