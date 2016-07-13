import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
    ('/bev', 'bev.Bev')
], debug=True)

app.router.add(webapp2.Route(r'/bev/<id:[0-9]+><:/?>', 'bev.BevInfo'))
app.router.add(webapp2.Route(r'/bev/all', 'bev.BevAll'))
app.router.add(webapp2.Route(r'/store', 'store.Store'))
app.router.add(webapp2.Route(r'/store/<id:[0-9]+><:/?>', 'store.StoreInfo'))
app.router.add(webapp2.Route(r'/store/all', 'store.StoreAll'))
app.router.add(webapp2.Route(r'/store/<sid:[0:9]+>/bev/<bid:[0:9]+><:/?>', 'store.StoreBevs'))
