from google.appengine.ext import ndb

import base_page
import db_defs


class Edit(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}

    def get(self):
        if self.request.get('type') == 'cider':
            cider_key = ndb.Key(urlsafe=self.request.get('key'))
            cider = cider_key.get()
            self.template_values['cider'] = cider
            stores = db_defs.Store.query(ancestor=ndb.Key(db_defs.Store, self.app.config.get('default-group')))
            store_boxes = []
            for s in stores:
                if s.key in cider.stores:
                    store_boxes.append({'name':s.name, 'key':s.key.urlsafe(), 'checked':True})
                else:
                    store_boxes.append({'name':s.name, 'key':s.key.urlsafe(), 'checked':False})
            self.template_values['stores'] = store_boxes
        self.render('edit.html', self.template_values)

    def post(self):
        cider_key = ndb.Key(urlsafe=self.request.get('key'))
        cider = cider_key.get()
        self.template_values['cider'] = cider
        name = self.request.get('cider_name')
        rating = self.request.get('rating')
        notes = self.request.get('notes')
        size = self.request.get('size')
        unit = self.request.get('unit')
        price = self.request.get('price')
        stores = [ndb.Key(urlsafe=x) for x in self.request.get_all('stores[]')]
        if name and rating and size and unit and price and stores:
            cider.name = name
            cider.rating = rating
            cider.notes = notes
            cider.size = int(size)
            cider.unit = unit
            cider.price = float(price)
            cider.stores = stores
            cider.put()
            self.template_values['ciders'] = [{'name': x.name, 'key': x.key.urlsafe()} for x in db_defs.Cider.query(ancestor=ndb.Key(db_defs.Cider, self.app.config.get('default-group'))).fetch()]
            self.template_values['stores'] = [{'name': x.name, 'key': x.key.urlsafe()} for x in db_defs.Store.query(ancestor=ndb.Key(db_defs.Store, self.app.config.get('default-group'))).fetch()]
            self.template_values['message'] = cider.name + ' has been updated'
            self.render('form.html', self.template_values)
        else:
            stores = db_defs.Store.query(ancestor=ndb.Key(db_defs.Store, self.app.config.get('default-group')))
            store_boxes = []
            for s in stores:
                if s.key in cider.stores:
                    store_boxes.append({'name':s.name, 'key':s.key.urlsafe(), 'checked':True})
                else:
                    store_boxes.append({'name':s.name, 'key':s.key.urlsafe(), 'checked':False})
            self.template_values['stores'] = store_boxes
            self.template_values['cider'] = cider
            self.template_values['message'] = 'All fields must be complete except notes.'
            self.render('edit.html', self.template_values)
