import webapp2
from google.appengine.ext import ndb
import db_defs
import json


class Bev(webapp2.RequestHandler):
    def post(self):
        # Creates a Beverage

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        new_bev = db_defs.Beverage()
        brand_name = self.request.get('brand_name', default_value=None)
        bev_name = self.request.get('bev_name', default_value=None)
        ratings = self.request.get_all('ratings[]', default_value=None)

        if brand_name and bev_name:
            new_bev.brand_name = brand_name
            new_bev.bev_name = bev_name
        else:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request"
            return

        if ratings:
            for r in ratings:
                new_rating = db_defs.Rating()
                new_rating.value = int(r)
                # new_rating.value = r['value']
                # new_rating.notes = r['notes']
                new_bev.ratings.append(new_rating)

        key = new_bev.put()
        out = new_bev.to_dict()
        self.response.write(json.dumps(out))
        return

    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        if 'id' in kwargs:
            out = ndb.Key(db_defs.Beverage, int(kwargs['id'])).get().to_dict()
            self.response.write(json.dumps(out))
        else:
            q = db_defs.Beverage.query()
            keys = q.fetch(keys_only=True)
            results = {'keys': [x.id() for x in keys]}
            self.response.write(json.dumps(results))


class BevInfo(webapp2.RequestHandler):
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        if 'id' in kwargs:
            id = self.request.get('id', default_value=None)
            beverage = db_defs.Beverage.get_by_id(id)
            beverage.id = id
            self.response.write(json.dumps(beverage))


class BevAll(webapp2.RequestHandler):

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


class BevInfo(webapp2.RedirectHandler):

    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return
        if 'id' in kwargs:
            result = ndb.Key(db_defs.Beverage, int(kwargs['id'])).get().to_dict()

            # NEEDS TO PULL INFORMATION FROM STORES THAT ARE RELATED TO THE CIDER
            self.response.write(json.dumps(result))




