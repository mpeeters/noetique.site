# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api
from Products.Five import BrowserView


class VideosView(BrowserView):

    @property
    def videos(self):
        brains = api.content.find(
            portal_type='Link',
            path='/'.join(self.context.getPhysicalPath()),
            review_state='published',
            sort_on='effective',
            sort_order='reverse',
        )
        videos =[]
        for b in brains:
            video = {
                'title': b.Title,
                'description': b.Description,
                'video_id': b.getRemoteUrl.split('?v=')[1] if '?v=' in b.getRemoteUrl else ''
            }
            videos.append(video)
        return videos
