import webapp2
from google.appengine.ext import ndb
import db_defs
import json


class Beverage(webapp2.RequestHandler):

    # Creates a Beverage
    def post(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        new_bev = db_defs.Beverage()
        brand_name = self.request.get('brand_name', default_value=None)
        bev_name = self.request.get('bev_name', default_value=None)

        if brand_name and bev_name:
            new_bev.brand_name = brand_name
            new_bev.bev_name = bev_name
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"
            return

        key = new_bev.put()
        if key:
            self.response.write(json.dumps(new_bev.to_dict()))
        return

    # Returns search results
    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        # Check if an ID is being used to pull a specific beverage
        results = {}
        bev_id = self.request.get('id', default_value=None)
        if bev_id:
            beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
            if beverage:
                results = beverage.to_dict()
        # Handle all other searches
        #TODO change to AND for query filter instead of OR
        else:
            # Pull all beverages from database
            query = db_defs.Beverage.query()
            # Filter query for search terms
            brand_name = self.request.get('brand_name', default_value=None)
            bev_name = self.request.get('bev_name', default_value=None)
            if brand_name:
                query = query.filter(db_defs.Beverage.brand_name == brand_name)
            if bev_name:
                query = query.filter(db_defs.Beverage.bev_name == bev_name)
            # Prepare for JSON and add ID so that users can more easily find entries
            results = []
            for q in query:
                b = q.to_dict()
                results.append(b)
        # Return results
        self.response.write(json.dumps(results))

    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            bev_id = int(kwargs['id'])
            bev_key = ndb.Key(db_defs.Beverage, int(bev_id))
            if bev_key:
                # Delete all references to the the beverage in the store price lists
                query = db_defs.Store.query()
                query = query.filter(db_defs.Store.price.beverage == bev_key)
                if query:
                    for q in query:
                        price = q.price
                        for p in price:
                            if p.beverage == bev_key:
                                q.price.remove(p)
                        q.put()

                # Delete beverage entity
                ndb.Key(db_defs.Beverage, bev_id).delete()


class AllBeveragesSimple(webapp2.RequestHandler):

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        query = db_defs.Beverage.query()
        results = []
        for x in query:
            bev = {}
            bev['bev_name'] = x.bev_name
            bev['brand_name'] = x.brand_name
            bev['id'] = x.key.id()
            results.append(bev)
        self.response.write(json.dumps(results))


class Rating(webapp2.RequestHandler):
    def put(self):

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        bev_id = self.request.get('bev_id', default_value=None)
        value = self.request.get('value', default_value=None)
        if bev_id and value:
            new_rating = db_defs.Rating()
            new_rating.value = int(value)
            notes = self.request.get('notes', default_value=None)
            if notes:
                new_rating.notes = notes

            beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
            if beverage:
                beverage.ratings.append(new_rating)
                key = beverage.put()
                out = beverage.to_dict()
                self.response.write(json.dumps(out))
            else:
                self.response.status_message = "Invalid Request: beverage does not exist"

        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"

        return
