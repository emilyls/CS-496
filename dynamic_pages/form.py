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
            size = self.request.get('size')
            cider.unit = self.request.get('unit')
            price = self.request.get('price')
            cider.stores = [ndb.Key(urlsafe=x) for x in self.request.get_all('stores[]')]
            cider.active = True
            if cider.name and cider.rating and size and cider.unit and price and cider.stores:
                cider.size = int(size)
                cider.price = float(price)
                cider.put()
                self.template_values['message'] = 'Added your review of ' + cider.name
            else:
                # cider.size = size
                # cider.price = price
                # stores = db_defs.Store.query(ancestor=ndb.Key(db_defs.Store, self.app.config.get('default-group')))
                # store_boxes = []
                # for s in stores:
                #     if s.key in cider.stores:
                #         store_boxes.append({'name': s.name, 'key': s.key.urlsafe(), 'checked': True})
                #     else:
                #         store_boxes.append({'name': s.name, 'key': s.key.urlsafe(), 'checked': False})
                # self.template_values['stores'] = store_boxes
                # self.template_values['cider'] = cider
                self.template_values['message'] = 'All fields must be complete except notes.'
        elif action == 'add_store':
            k = ndb.Key(db_defs.Store, self.app.config.get('default-group'))
            store = db_defs.Store(parent=k)
            store.name = self.request.get('store_name')
            if not store.name:
                self.template_values['message'] = 'No store name was entered'
            else:
                store.put()
                self.template_values['message'] = 'Added ' + store.name + ' the list of stores.'
        elif action == 'edit':
            cider_key = ndb.Key(urlsafe=self.request.get('key'))
            cider = cider_key.get()
            cider.name = self.request.get('cider_name')
            cider.rating = self.request.get('rating')
            cider.notes = self.request.get('notes')
            size = self.request.get('size')
            cider.unit = self.request.get('unit')
            price = self.request.get('price')
            cider.stores = [ndb.Key(urlsafe=x) for x in self.request.get_all('stores[]')]
            if cider.name and cider.rating and size and cider.unit and price and cider.stores:
                cider.size = int(size)
                cider.price = float(price)
                cider.put()
            else:
                self.template_values['message'] = 'All fields must be complete except notes.'
        else:
            self.template_values['message'] = 'Action ' + action + ' is unknown'
        self.render('form.html')
