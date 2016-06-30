from google.appengine.ext import ndb


class Message(ndb.Model):
    channel = ndb.StringProperty(required=True)
    date_time = ndb.DateTimeProperty(required=True)
    count = ndb.IntegerProperty(required=True)


class Channel(ndb.Model):
    name = ndb.StringProperty(required=True)
    classes = ndb.StringProperty(repeated=True)     # list of strings
    active = ndb.BooleanProperty(required=True)
    icon = ndb.BlobProperty()


class ChannelClass(ndb.Model):
    name = ndb.StringProperty(required=True)
