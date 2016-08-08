import webapp2
from google.appengine.ext import ndb
import db_defs
import json
from oauth2client import client, crypt


def add_favorite(favorites, key):
    for fav in favorites:
        if key == fav.bev_key:
            return
    new_fav = db_defs.Favorite()
    new_fav.bev_key = key
    new_fav.user_notes = ""
    favorites.append(new_fav)
    return


def get_bev_info(favorites):
    results = []
    for bev in favorites:
        bev_key = bev.bev_key
        beverage = db_defs.Beverage.query(db_defs.Beverage.key == bev_key).get()
        beverage = beverage.to_dict()
        beverage['user_notes'] = bev.user_notes
        results.append(beverage)
    return results


def add_notes(user, bev_key, notes):
    for i in range(len(user.favorites)):
        if user.favorites[i].bev_key == bev_key:
            user.favorites[i].user_notes = notes
            return user.put()


class User(webapp2.RequestHandler):

    def post(self):
        client_id = "957738399987-9epk0j4jne0mgm829q0mhh5sec3cqbhd.apps.googleusercontent.com"

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.message = "Invalid Request: This API only supports JSON"
            return

        # id_token = self.request.get('id_token', default_value=None)
        # if id_token:
        #     try:
        #         id_info = client.verify_id_token(id_token, client_id)
        #         user_email = id_info['email']
        user_email = "snyderem@oregonstate.edu"
        user = db_defs.User.query(db_defs.User.email == user_email).get()

        favorite_id = self.request.get('favorite_id', default_value=None)
        favorite_bev = ''
        if favorite_id:
            try:
                favorite_id = int(favorite_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid value"
                return
            favorite_bev = ndb.Key(db_defs.Beverage, int(favorite_id))

        if user:
            if favorite_bev:
                add_favorite(user.favorites, favorite_bev)
                key = user.put()
            self.response.status = 200
            # self.response.write(json.dumps(query['favorites']))
            self.response.write(json.dumps(get_bev_info(user.favorites)))
        else:
            new_user = db_defs.User()
            new_user.email = user_email
            new_user.favorites = []
            if favorite_bev:
                add_favorite(new_user.favorites, favorite_bev)
            key = new_user.put()
            if key:
                self.response.status = 200
                self.response.write(json.dumps(get_bev_info(new_user.favorites)))

            # except crypt.AppIdentityError:
                # Invalid token
                # self.response.status = 401  # bad request
                # self.response.message = "Unauthorized, invalid token"
        # else:
        #     self.response.status = 401
        #     self.response.message = "Unauthorized, no token sent"

        return

    def put(self):
        client_id = "957738399987-9epk0j4jne0mgm829q0mhh5sec3cqbhd.apps.googleusercontent.com"

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.message = "Invalid Request: This API only supports JSON"
            return

        # id_token = self.request.get('id_token', default_value=None)
        # if id_token:
        #     try:
        #         id_info = client.verify_id_token(id_token, client_id)
        #         user_email = id_info['email']
        user_email = "snyderem@oregonstate.edu"
        user = db_defs.User.query(db_defs.User.email == user_email).get()
        favorite_id = self.request.get('favorite_id', default_value=None)
        user_notes = self.request.get('user_notes', default_value=None)

        if favorite_id and user_notes and user:
            try:
                favorite_id = int(favorite_id)
            except ValueError:
                self.response.status = 400
                self.response.status_message = "Invalid Request: invalid value"
                return
            favorite_bev = ndb.Key(db_defs.Beverage, int(favorite_id))
            if favorite_bev:
                key = add_notes(user, favorite_bev, user_notes)
                if key:
                    self.response.status = 200
                    self.response.write(json.dumps(get_bev_info(user.favorites)))
            else:
                self.response.status = 400
                self.response.write("Invalid beverage id")

        else:
            self.response.status = 400
            self.response.write("Invalid Data")

                # except crypt.AppIdentityError:
                # Invalid token
                # self.response.status = 401  # bad request
                # self.response.message = "Unauthorized, invalid token"
        # else:
        #     self.response.status = 401
        #     self.response.message = "Unauthorized, no token sent"

        return


