import webapp2

app = webapp2.WSGIApplication([
    ('/Beverage', 'beverage.Beverage')
], debug=True)


app.router.add(webapp2.Route(r'/Beverage/<id:[0-9]+><:/?>', 'beverage.Beverage'))
app.router.add(webapp2.Route(r'/AllBeveragesSimple', 'beverage.AllBeveragesSimple'))
app.router.add(webapp2.Route(r'/Store', 'store.Store'))
app.router.add(webapp2.Route(r'/Store/<id:[0-9]+><:/?>', 'store.Store'))
app.router.add(webapp2.Route(r'/StoreDeleteBeverage/<sid:[0-9]+><:/?>/<bid:[0-9]+><:/?>', 'store.StoreDeleteBeverage'))
app.router.add(webapp2.Route(r'/AllStoresSimple', 'store.AllStoresSimple'))
app.router.add(webapp2.Route(r'/Rating', 'beverage.Rating'))
app.router.add(webapp2.Route(r'/Price', 'store.Price'))
app.router.add(webapp2.Route(r'/User', 'users.User'))

