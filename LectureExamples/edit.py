from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import base_page
import db_defs


class Edit(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, request)
        self.template_values = {}
        self.template_values['edit_url'] = blobstore.create_upload_url('/edit/channel')

    def get(self):
        if self.request.get('type') == 'channel':
            channel_key = ndb.Key(urlsafe=self.request.get('key'))
            channel = channel_key.get()
            if channel.icon:
                self.template_values['img_url'] = images.get_serving_url(channel.icon, crop=True, size=64)
            self.template_values['channel'] = channel
            classes = db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group')))
            class_boxes = []
            for c in classes:
                if c.key in channel.classes:
                    class_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':True})
                else:
                    class_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':False})
            self.template_values['classes'] = class_boxes
        self.render('edit.html', self.template_values)