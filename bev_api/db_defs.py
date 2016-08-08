from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    favorites = ndb.KeyProperty(repeated=True)

    def to_dict(self):
        d = {}
        d['email'] = self.email
        d['id'] = self.key.id()
        return d


class Rating(ndb.Model):
    value = ndb.FloatProperty(required=True)
    notes = ndb.TextProperty()


class Beverage(ndb.Model):
    brand_name = ndb.StringProperty(required=True)
    bev_name = ndb.StringProperty(required=True)
    ratings = ndb.StructuredProperty(Rating, repeated=True)

    def to_dict(self):
        d = {}
        d['brand_name'] = self.brand_name
        d['bev_name'] = self.bev_name
        d['ratings'] = [r.to_dict() for r in self.ratings]
        d['id'] = self.key.id()
        return d

    def to_simple_dict(self):
        d = {}
        d['brand_name'] = self.brand_name
        d['bev_name'] = self.bev_name
        d['id'] = self.key.id()
        return d


class Date(ndb.Model):
    day = ndb.IntegerProperty(required=True)
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

    def to_dict(self):
        d = {}
        d['beverage'] = self.beverage.id()  # Need this to be able to convert the key to JSON
        d['price'] = self.price
        d['size'] = self.size
        d['date'] = self.date.to_dict()
        d['units'] = self.units
        return d


class Store(ndb.Model):
    name = ndb.StringProperty(required=True)
    address = ndb.StructuredProperty(Address, required=True)
    price = ndb.StructuredProperty(Price, repeated=True)

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['address'] = self.address.to_dict()
        d['prices'] = [p.to_dict() for p in self.price]
        d['id'] = self.key.id()
        return d

    def to_simple_dict(self):
        d = {}
        d['name'] = self.name
        d['address'] = self.address.to_dict()
        d['id'] = self.key.id()
        return d
