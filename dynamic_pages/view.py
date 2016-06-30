from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import base_page
import db_defs


class View(base_page.BaseHandler):
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
        self.render('view.html', self.template_values)