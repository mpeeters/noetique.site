# -*- coding: utf-8 -*-

from plone import api
from Products.Five import BrowserView


class HomeView(BrowserView):

    @property
    def portal_path(self):
        portal = api.portal.get()
        return '/'.join(portal.getPhysicalPath())

    @property
    def last_articles(self):
        brains = api.content.find(
            portal_type=('Document', 'File'),
            path=self.portal_path + '/billets',
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
            sort_limit=3
        )
        if len(brains) < 1:
            return None

        articles =[]
        for b in brains[:3]:
            article = {
                'title': b.Title,
                'description': b.Description,
                'url': b.getURL()+'/view',
                'effective': b.effective,
            }
            articles.append(article)
        return articles


    @property
    def last_news(self):
        brains = api.content.find(
            portal_type='News Item',
            path=self.portal_path + '/actualites',
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
            sort_limit=3
        )
        if len(brains) < 1:
            return None

        brain = brains[0]
        return {
            'title': brain.Title,
            'description': brain.Description,
            'url': brain.getURL(),
            'effective': brain.effective,
        }

    @property
    def last_thought(self):
        brains = api.content.find(
            portal_type='Document',
            path=self.portal_path + '/journal',
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
            sort_limit=3
        )
        if len(brains) < 1:
            return None

        brain = brains[0]
        return {
            'title': brain.Title,
            'description': brain.Description,
            'url': brain.getURL(),
            'effective': brain.effective,
        }

    @property
    def next_events(self):
        pass

    @property
    def last_books(self):
        brains = api.content.find(
            portal_type='noetique.site.Book',
            path=self.portal_path + '/livres',
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
            sort_limit=3
        )
        books =[]
        for b in brains[:3]:
            obj = b.getObject()
            book = {
                'title': obj.title,
                'description': obj.description,
                'author': obj.author,
                'publisher': obj.publisher,
                'year': obj.year,
                'url': obj.absolute_url(),
            }
            books.append(book)
        return books

    @property
    def last_video(self):
        brains = api.content.find(
            portal_type='Link',
            path=self.portal_path + '/videos',
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
            sort_limit=3
        )
        if len(brains) < 1:
            return None

        link = brains[0].getObject()
        video = {
            'title': link.title,
            'description': link.description,
            'video_id': link.remoteUrl.split('?v=')[1] if '?v=' in link.remoteUrl else ''
        }
        return video