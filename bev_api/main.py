import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
    ('/Beverage', 'beverage.Beverage')
], debug=True)


app.router.add(webapp2.Route(r'/Store', 'store.Store'))
app.router.add(webapp2.Route(r'/StoreDeleteBeverage', 'store.StoreDeleteBeverage'))
app.router.add(webapp2.Route(r'/AllBeveragesSimple', 'beverage.AllBeveragesSimple'))
app.router.add(webapp2.Route(r'/AllStoresSimple', 'store.AllStoresSimple'))
# app.router.add(webapp2.Route(r'/BeverageInfo/<id:[0-9]+><:/?>', 'beverage.BevInfo'))
# app.router.add(webapp2.Route(r'/StoreInfo/<id:[0-9]+><:/?>', 'store.StoreInfo'))
app.router.add(webapp2.Route(r'/Rating', 'beverage.Rating'))
app.router.add(webapp2.Route(r'/Price', 'store.Price'))

# app.router.add(webapp2.Route(r'/bevdelete/<id:[0-9]+><:/?>', 'bev.BevDelete'))
# app.router.add(webapp2.Route(r'/bev/all', 'bev.BevAll'))
# app.router.add(webapp2.Route(r'/storedelete/<id:[0-9]+><:/?>', 'store.StoreDelete'))
# app.router.add(webapp2.Route(r'/store/all', 'store.StoreAll'))
# app.router.add(webapp2.Route(r'/store/<sid:[0:9]+>/bev/<bid:[0:9]+><:/?>', 'store.StoreBevs'))
