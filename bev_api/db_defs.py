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


class Beverage(ndb.Model):
    brand_name = ndb.StringProperty(required=True)
    bev_name = ndb.StringProperty(required=True)
    ratings = ndb.StructuredProperty(Rating, repeated=True)


class Address(ndb.Model):
    street = ndb.StringProperty()
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)


class Price(Model):
    beverage = ndb.KeyProperty(required=True)
    price = ndb.FloatProperty(required=True)
    date = ndb.DateProperty(required=True)
    size = ndb.IntegerProperty(required=True)
    units = ndb.StringProperty(required=True)

    def to_dict(self):
        d = super(Price, self).to_dict()
        d['beverage'] = d['beverage'].id
        return d


class Store(ndb.Model):
    name = ndb.StringProperty(required=True)
    address = ndb.StructuredProperty(Address, required=True)
    price = ndb.StructuredProperty(Price, required=True)

