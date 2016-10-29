# -*- coding: utf-8 -*-

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile.field import NamedBlobImage
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
    description = schema.Text(
        title=u"Bref descriptif du livre",
        required=True,
    )
    author = schema.TextLine(
        title=u"Auteur(s)",
        required=False
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

    # widgets
    directives.widget('description', rows=5)
    directives.widget('summary', rows=15)
    directives.widget('foreword', rows=15)
    
    # fieldsets
    model.fieldset(
        'summary',
        label=u"Résumé/Préface",
        fields=['cover', 'summary', 'foreword']
    )


class Book(Item):
    implements(IBook)

