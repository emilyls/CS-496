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
            self.response.status = 400
            self.response.status_message = "Invalid Request"
            return

        key = new_bev.put()
        if key:
            self.response.write(json.dumps(new_bev.to_dict()))
        else:
            self.response.status = 500
            self.response.status_message = "Internal Server Error"
        return

    # Returns search results
    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        # Pull all beverages from database
        query = db_defs.Beverage.query()
        # Filter query for search terms
        brand_name = self.request.get('brand_name', default_value=None)
        bev_name = self.request.get('bev_name', default_value=None)
        bev_id = self.request.get('id', default_value=None)
        if bev_id:
            # Make sure bev_id is a valid integer
            try:
                bev_id = int(bev_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid bev_id"
                return
            bev_key = ndb.Key(db_defs.Beverage, bev_id)
            query = query.filter(db_defs.Beverage.key == bev_key)
        if brand_name:
            query = query.filter(db_defs.Beverage.brand_name == brand_name)
        if bev_name:
            query = query.filter(db_defs.Beverage.bev_name == bev_name)
        # Prepare for JSON
        results = []
        for q in query:
            b = q.to_dict()
            results.append(b)
        # Return results
        self.response.write(json.dumps(results))

    # Deletes a beverage and all references to it in the store entities
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            bev_id = int(kwargs['id'])
            bev_key = ndb.Key(db_defs.Beverage, bev_id)
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
        else:
            self.response.status = 400
            self.response.status_message = "Invalid Request: must specify id"


class AllBeveragesSimple(webapp2.RequestHandler):

    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        query = db_defs.Beverage.query()
        results = [q.to_simple_dict() for q in query]
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
            # Make sure the value is a valid float in the needed range
            try:
                new_rating.value = float(value)
                if new_rating.value < 0 or new_rating.value > 10:
                    self.response.status = 400
                    self.response.status_message = "Invalid Request: value out of range"
                    return
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid value"
                return
            notes = self.request.get('notes', default_value=None)
            if notes:
                new_rating.notes = notes

            # Make sure the beverage id is a valid integer
            try:
                bev_id = int(bev_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid value"
                return
            beverage = ndb.Key(db_defs.Beverage, int(bev_id)).get()
            # Make sure that the beverage exists
            if beverage:
                beverage.ratings.append(new_rating)
                key = beverage.put()
                if key:
                    self.response.write(json.dumps(beverage.to_dict()))
                else:
                    self.response.status = 500
                    self.response.status_message = "Internal Server Error"

            else:
                self.response.status = 400
                self.response.status_message = "Invalid Request: beverage does not exist"

        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"

        return
