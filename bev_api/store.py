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
        street = self.request.get('street', default_value=None)
        city = self.request.get('city', default_value=None)
        state = self.request.get('state', default_value=None)
        country = self.request.get('country', default_value=None)

        if name and street and city and state and country:
            new_store.name = name
            new_address = db_defs.Address()
            new_address.street = street
            new_address.city = city
            new_address.state = state
            new_address.country = country
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

    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            result = ndb.Key(db_defs.Store, int(kwargs['id'])).get().to_dict()

            # TODO NEEDS TO PULL INFORMATION FROM STORES THAT ARE RELATED TO THE CIDER
            self.response.write(json.dumps(result))

    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            ndb.Key(db_defs.Store, int(kwargs['id'])).delete()


class AllStoresSimple(webapp2.RequestHandler):

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


class Price(webapp2.RequestHandler):
    def put(self):
        # Creates a Beverage
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        new_price = db_defs.Price()
        store_id = self.request.get('store_id', default_value=None)
        bev_id = self.request.get('bev_id', default_value=None)
        price = self.request.get('price', default_value=None)
        date = self.request.get('date', default_value=None)
        size = self.request.get('size', default_value=None)
        units = self.request.get('units', default_value=None)

        if bev_id and store_id and price and date and size and units:
            new_price.price = price
            new_price.date = date
            new_price.size = size
            new_price.units = units
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"
            return
        beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
        new_price.beverage = beverage.key()
        store = ndb.Key(db_defs.Store, int(store_id)).get()
        store.price.append(new_price)
        key = store.put()
        out = store.to_dict()
        self.response.write(json.dumps(out))
        return
