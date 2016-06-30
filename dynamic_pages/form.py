from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import base_page
import db_defs


class Add(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}

    def render(self, page):
        self.template_values['ciders'] = [{'name':x.name, 'key':x.key.urlsafe()}
                                           for x in db_defs.Cider.query(ancestor=ndb.Key(db_defs.Cider, self.app.config.get('default-group'))).fetch()]
        self.template_values['stores'] = [{'name':x.name, 'key':x.key.urlsafe()}
                                            for x in db_defs.Store.query(ancestor=ndb.Key(db_defs.Store, self.app.config.get('default-group'))).fetch()]
        base_page.BaseHandler.render(self, page, self.template_values)

    def get(self):
        self.render('form.html')

    def post(self):
        action = self.request.get('action')
        if action == 'add_cider':
            k = ndb.Key(db_defs.Cider, self.app.config.get('default-group'))
            cider = db_defs.Cider(parent=k)
            cider.name = self.request.get('cider_name')
            cider.rating = self.request.get('rating')
            cider.notes = self.request.get('notes')
            cider.size = int(self.request.get('size'))
            cider.unit = self.request.get('unit')
            cider.price = float(self.request.get('price'))
            cider.stores = [ndb.Key(urlsafe=x) for x in self.request.get_all('stores[]')]
            cider.active = True
            cider.put()
            self.template_values['message'] = 'Added ' + cider.name + ' to the database'
        elif action == 'add_store':
            k = ndb.Key(db_defs.Store, self.app.config.get('default-group'))
            store = db_defs.Store(parent=k)
            store.name = self.request.get('store_name')
            store.put()
            self.template_values['message'] = 'Added ' + store.name + '(store) to the database'
        elif action == 'edit':
            cider_key = ndb.Key(urlsafe=self.request.get('key'))
            cider = cider_key.get()
            cider.name = self.request.get('cider_name')
            cider.rating = self.request.get('rating')
            cider.notes = self.request.get('notes')
            cider.size = int(self.request.get('size'))
            cider.unit = self.request.get('unit')
            cider.price = float(self.request.get('price'))
            cider.stores = [ndb.Key(urlsafe=x) for x in self.request.get_all('stores[]')]
            cider.put()
            self.template_values['message'] = cider.name + ' has been updated'
        else:
            self.template_values['message'] = 'Action ' + action + ' is unknown'
        self.render('form.html')
