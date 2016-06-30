from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import base_page
import db_defs


class Admin(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}
        self.template_values['upload_url'] = blobstore.create_upload_url('/channel/add')

    def render(self, page):
        self.template_values['classes'] = [{'name':x.name, 'key':x.key.urlsafe()}
                                           for x in db_defs.ChannelClass.query().fetch()]
        self.template_values['channels'] = [{'name':x.name, 'key':x.key.urlsafe()}
                                            for x in db_defs.Channel.query().fetch()]       # query(ancestor=ndb.Key(db_defs.Channel, self.app.config.get('default-group')))
        base_page.BaseHandler.render(self, page, self.template_values)

    def get(self):
        self.render('admin.html')

    def post(self, icon_key=None):
        action = self.request.get('action')
        if action == 'add_channel':
            k = ndb.Key(db_defs.Channel, self.app.config.get('default-group'))
            chan = db_defs.Channel(parent=k)
            chan.name = self.request.get('channel-name')
            chan.classes = [ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
            chan.active = True
            chan.icon = icon_key
            chan.put()
            self.template_values['message'] = 'Added channel ' + chan.name + ' to the database'
        elif action == 'add_class':
            k = ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))
            c = db_defs.ChannelClass(parent=k)
            c.name = self.request.get('class-name')
            c.put()
            self.template_values['message'] = 'Added class ' + c.name + 'to the database'
        else:
            self.template_values['message'] = 'Action ' + action + ' is unknown'
        self.render('admin.html')
