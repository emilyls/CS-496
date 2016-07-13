import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Mod(webapp2.RequestHandler):
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "Not Acceptable, API only supports json"
            return
        if 'id' in kwargs:
            out = ndb.Key(db_models.Mod, int(kwargs['id'])).get().to_dict()
            self.response.write(json.dumps(out))
        else:
            q = db_models.Mod.query()
            keys = q.fetch(keys_only=True)
            results = { 'keys' : [x.id() for x in keys ]}
            self.response.write(json.dumps(results))



# Curl Tests

# curl --data "nick=ANewMod" -H "Accept: application/json" http://localhost:8080/mod
# curl -H "Accept: application/json" http://localhost:8080/mod/1234562345125
# curl --data-urlencode "name=Test Channel" --data-urlencode "topics[]=topic1" --data-urlencode "topics[]=topic 2" -d "mods[]=1234 -d "mods[]=2345" -H "Accept: application/json" http://localhost:8080/channel
# curl -X PUT -H "Accept: application/json" http://localhost:8080/channel/123412/mod/1231234
