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
        out = new_bev.to_dict()
        new_bev['id'] = key
        self.response.write(json.dumps(out))
        return

    # Returns search results
    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        # Check if an ID is being used to pull a specific beverage
        bev_id = self.request.get('id', default_value=None)
        if bev_id:
            beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
            results = beverage.to_dict()
            results['id'] = bev_id
        # Handle all other searches
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
                b['id'] = q.key.id()
                results.append(b)
        # Return results
        self.response.write(json.dumps(results))

    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            ndb.Key(db_defs.Beverage, int(kwargs['id'])).delete()

            # TODO delete all store references to the beverage


class AllBeveragesSimple(webapp2.RequestHandler):

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        query = db_defs.Beverage.query()
        query = query.fetch(projection=[db_defs.Beverage.bev_name, db_defs.Beverage.brand_name])
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
        # Creates a Beverage
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        new_rating = db_defs.Rating()
        bev_id = self.request.get('id', default_value=None)
        value = self.request.get('value', default_value=None)
        notes = self.request.get('notes', default_value=None)

        if bev_id and value:
            new_rating.value = value
            if notes:
                new_rating.notes = notes
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"
            return
        beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
        beverage.rating.append(new_rating)
        key = beverage.put()
        out = beverage.to_dict()
        self.response.write(json.dumps(out))
        return
