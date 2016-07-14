import webapp2
from google.appengine.ext import ndb
import db_defs
import json
import datetime


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
        out['id'] = key.id()
        self.response.write(json.dumps(out))
        return

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        # Check if an ID is being used to pull a specific store
        store_id = self.request.get('id', default_value=None)
        if store_id:
            store = ndb.Key(db_defs.Store, int(store_id)).get()
            results = store.to_dict()
            results['id'] = store_id
        else:
            # Pull all stores from database
            query = db_defs.Store.query()

            # Filter query for search terms
            store_name = self.request.get('store_name', default_value=None)
            street = self.request.get('street', default_value=None)
            city = self.request.get('city', default_value=None)
            state = self.request.get('state', default_value=None)
            country = self.request.get('country', default_value=None)
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

            # TODO Verify if Beverage info is handled appropriately
            # Beverages
            brand_name = self.request.get('brand_name', default_value=None)
            bev_name = self.request.get('bev_name', default_value=None)
            if brand_name or bev_name:
                bev_query = db_defs.Beverage.query()
                bev_query = query.filter(db_defs.Beverage.brand_name == brand_name)
                bev_query = query.filter(db_defs.Beverage.bev_name == bev_name)
                if bev_query:
                    for bev in bev_query:
                        query = query.filter(db_defs.Store.price.beverage == bev.key)

            results = []
            for q in query:
                s = q.to_dict()
                s['id'] = q.key.id()
                results.append(s)

        self.response.write(json.dumps(results))

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

        store_id = self.request.get('store_id', default_value=None)
        bev_id = self.request.get('bev_id', default_value=None)
        price = self.request.get('price', default_value=None)
        month = self.request.get('month', default_value=None)
        year = self.request.get('year', default_value=None)
        size = self.request.get('size', default_value=None)
        units = self.request.get('units', default_value=None)
        if bev_id and store_id and price and month and year and size and units:
            new_price = db_defs.Price()
            new_price.price = float(price)
            new_price.size = float(size)
            new_price.units = units

            new_date = db_defs.Date()
            new_date.month = int(month)
            new_date.year = int(year)

            new_price.date = new_date

            beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
            new_price.beverage = beverage.key
            store = ndb.Key(db_defs.Store, int(store_id)).get()
            store.price.append(new_price)

            key = store.put()
            out = store.to_dict()
            out['id'] = key
            self.response.write(json.dumps(out))
            # self.response.write(out)
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"

        return
