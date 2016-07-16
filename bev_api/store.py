import webapp2
from google.appengine.ext import ndb
import db_defs
import json


class Store(webapp2.RequestHandler):
    # Creates a Store
    def post(self):
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
            key = new_store.put()
            if key:
                self.response.write(json.dumps(new_store.to_dict()))
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"

        return

    # Returns search results
    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        results = {}
        query = db_defs.Store.query()

        # Filter query for search terms
        store_id = self.request.get('store_id', default_value=None)
        store_name = self.request.get('store_name', default_value=None)
        street = self.request.get('street', default_value=None)
        city = self.request.get('city', default_value=None)
        state = self.request.get('state', default_value=None)
        country = self.request.get('country', default_value=None)
        if store_id:
            try:
                store_id = int(store_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid store_id"
                return
            store_key = ndb.Key(db_defs.Store, store_id)
            query = query.filter(db_defs.Store.key == store_key)
        if store_name:
            query = query.filter(db_defs.Store.name == store_name)
        if street:
            query = query.filter(db_defs.Store.address.street == street)
        if city:
            query = query.filter(db_defs.Store.address.city == city)
        if state:
            query = query.filter(db_defs.Store.address.state == state)
        if country:
            query = query.filter(db_defs.Store.address.country == country)

        # Beverage by ID
        bev_id = self.request.get('bev_id', default_value=None)
        if bev_id:
            try:
                bev_id = int(bev_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid bev_id"
                return
            bev_key = ndb.Key(db_defs.Beverage, bev_id)
            if bev_key:
                query = query.filter(db_defs.Store.price.beverage == bev_key)
            else:
                query = []
        results = [q.to_dict() for q in query]

        self.response.write(json.dumps(results))

    # Deletes a store
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            try:
                store_id = int(kwargs['id'])
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid store_id"
                return
            ndb.Key(db_defs.Store, store_id).delete()


class AllStoresSimple(webapp2.RequestHandler):

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        query = db_defs.Store.query()
        results = [q.to_simple_dict() for q in query]
        self.response.write(json.dumps(results))


class Price(webapp2.RequestHandler):

    def put(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        store_id = self.request.get('store_id', default_value=None)
        bev_id = self.request.get('bev_id', default_value=None)
        price = self.request.get('price', default_value=None)
        day = self.request.get('day', default_value=None)
        month = self.request.get('month', default_value=None)
        year = self.request.get('year', default_value=None)
        size = self.request.get('size', default_value=None)
        units = self.request.get('units', default_value=None)
        if bev_id and store_id and price and day and month and year and size and units:
            new_price = db_defs.Price()
            new_date = db_defs.Date()

            # test that all integers / floats are valid values
            try:
                new_price.price = float(price)
                new_price.size = float(size)
                new_price.day = int(day)
                new_date.month = int(month)
                new_date.year = int(year)
                bev_id = int(bev_id)
                store_id = int(store_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid value"
                return

            new_price.units = units
            new_price.date = new_date

            beverage = ndb.Key(db_defs.Beverage, bev_id).get()
            store = ndb.Key(db_defs.Store, store_id).get()
            # Make sure that the beverage and the store ids are valid and that both exist
            if beverage and store:
                new_price.beverage = beverage.key
                store.price.append(new_price)
                key = store.put()
                if key:
                    self.response.write(json.dumps(store.to_dict()))
                else:
                    self.response.status = 500
                    self.response.status_message = "Internal Server Error"
            else:
                self.response.status = 400
                self.response.status_message = "Invalid Request"
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: missing filed"

        return


class StoreDeleteBeverage(webapp2.RequestHandler):
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if ('sid' in kwargs) and ('bid' in kwargs):
            store = ndb.Key(db_defs.Store, int(kwargs['sid'])).get()
            beverage = ndb.Key(db_defs.Beverage, int(kwargs['bid'])).get()
            # Check that both the store and beverage ids are valid
            if store and beverage:
                # Remove the beverage from the store's price list
                for p in store.price:
                    if p.beverage == beverage.key:
                        store.price.remove(p)
                key = store.put()
                if key:
                    self.response.write(json.dumps(store.to_dict()))
                else:
                    self.response.status = 500
                    self.response.status_message = "Internal Server Error"
            else:
                self.response.status = 400
                self.response.status_message = "Invalid Request: missing field"
        return
