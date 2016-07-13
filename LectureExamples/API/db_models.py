class Channel(Model):
    name = ndb.StringProperty(required=True)
    topic = ndb.StringProperty(repeated=True)
    mods = ndb.KeyProperty(repeated=True)
    update = ndb.StructuredProperty(Update, repeated=True)

    def to_dict(self):
        d = super(Channel, self).to_dict()
        d['mods'] = [m.id() for m in d['mods']]
        return d