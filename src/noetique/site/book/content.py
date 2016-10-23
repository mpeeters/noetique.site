# -*- coding: utf-8 -*-

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
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
        title=u"Résumé court du livre",
        required=True,
    )
    comment = schema.Text(
        title=u"Commentaire sur le livre",
        required=False,
    )
    summary = RichText(
        title=u"Résumé détaillé du livre",
        required=False,
    )
    author = schema.TextLine(
        title=u"Auteur(s)",
        required=False
    )
    fourthcover = RichText(
        title=u"4ème de couverture",
        required=False,
    )
    foreword = RichText(
        title=u"Préface du livre",
        required=False,
    )
    afterward = RichText(
        title=u"Postface du livre",
        required=False,
    )

    # widgets
    directives.widget('description', rows=7)
    directives.widget('comment', rows=7)
    directives.widget('summary', rows=15)
    directives.widget('fourthcover', rows=15)
    directives.widget('foreword', rows=15)
    directives.widget('afterward', rows=15)
    
    # fieldsets
    model.fieldset(
        'prepost',
        label=u"4ème/Pré/Post",
        fields=['fourthcover', 'foreword', 'afterward']
    )


class Book(Item):
    implements(IBook)

