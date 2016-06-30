from google.appengine.ext import ndb


class Cider(ndb.Model):
    name = ndb.StringProperty(required=True)
    rating = ndb.StringProperty(required=True)
    notes = ndb.TextProperty()
    size = ndb.IntegerProperty(required=True)
    unit = ndb.StringProperty(required=True)
    price = ndb.FloatProperty(required=True)
    stores = ndb.KeyProperty(repeated=True)
    active = ndb.BooleanProperty(required=True)


class Store(ndb.Model):
    name = ndb.StringProperty(required=True)


