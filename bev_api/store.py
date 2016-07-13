import webapp2
from google.appengine.ext import ndb
import db_defs
import json


class Store(webapp2.RequestHandler):

    def post(self):
        # Creates a Store

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        new_store = db_defs.Store()
        name = self.request.get('name', default_value=None)
        address = self.request.get('address', default_value=None)

        if name and address:
            new_store.name = name
            new_address = db_defs.Address()
            new_address.street = address
            new_store.address = new_address
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"
            return

        # TODO: Handle prices

        key = new_store.put()
        out = new_store.to_dict()
        self.response.write(json.dumps(out))
        return


# class StoreInfo(webapp2.RequestHandler):
#
#     def get(self, **kwargs):
#         if 'application/json' not in self.request.accept:
#             self.response.status = 400  # bad request
#             self.response.status_message = "Invalid Request: This API only supports JSON"
#             return
#
#         if 'id' in kwargs:
#             id = self.request.get('id', default_value=None)
#             store = db_defs.Store.get_by_id(id)
#             store.id = id
#             self.response.write(json.dumps(store))


class StoreAll(webapp2.RequestHandler):

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        query = db_defs.Store.query()
        query = query.fetch(projection=[db_defs.Store.name, db_defs.Store.address.street])
        results = []
        for x in query:
            store = {}
            store['name'] = x.name
            # TODO need to get address to work
            store['address'] = x.address.street
            store['id'] = x.key.id()
            results.append(store)
        self.response.write(json.dumps(results))


class StoreInfo(webapp2.RedirectHandler):

    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            result = ndb.Key(db_defs.Store, int(kwargs['id'])).get().to_dict()

            # TODO NEEDS TO PULL INFORMATION FROM STORES THAT ARE RELATED TO THE CIDER
            self.response.write(json.dumps(result))





