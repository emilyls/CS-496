from google.appengine.ext import ndb


# LECTURE CODE NEED LOTS OF COMMENTS
# Needed in order to JSONify the key
class Model(ndb.Model):
    def to_dict(self):
        d = super(Model, self).to_dict()
        d['key'] = self.key.id()
        return d


class Rating(ndb.Model):
    value = ndb.IntegerProperty(required=True)
    notes = ndb.TextProperty()


class Beverage(Model):
    brand_name = ndb.StringProperty(required=True)
    bev_name = ndb.StringProperty(required=True)
    ratings = ndb.StructuredProperty(Rating, repeated=True)


class Date(ndb.Model):
    month = ndb.IntegerProperty(required=True)
    year = ndb.IntegerProperty(required=True)


class Address(ndb.Model):
    street = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)


class Price(ndb.Model):
    beverage = ndb.KeyProperty(required=True)
    price = ndb.FloatProperty(required=True)
    date = ndb.StructuredProperty(Date, required=True)
    size = ndb.FloatProperty(required=True)
    units = ndb.StringProperty(required=True)


class Store(Model):
    name = ndb.StringProperty(required=True)
    address = ndb.StructuredProperty(Address, required=True)
    price = ndb.StructuredProperty(Price, repeated=True)


