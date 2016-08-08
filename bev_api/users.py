import webapp2
import ndb
import db_defs
import json
from oauth2client import client, crypt


class User(webapp2.RequestHandler):

    def post(self):
        client_id = "957738399987-9epk0j4jne0mgm829q0mhh5sec3cqbhd.apps.googleusercontent.com"

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.message = "Invalid Request: This API only supports JSON"
            return

        id_token = self.request.get('id_token', default_value=None)
        if id_token:
            try:
                id_info = client.verify_id_token(id_token, client_id)
                user_email = id_info['email']
                query = db_defs.User.query(db_defs.User.email == user_email).get()

                favorite_id = self.request.get('favorite_id', default_value=None)
                if favorite_id:
                    # Make sure the beverage id is a valid integer
                    try:
                        favorite_id = int(favorite_id)
                    except ValueError:
                        self.response.status = 400
                        self.response.status_message = "Invalid Request: invalid value"
                        return
                    favorite_bev = ndb.Key(db_defs.Beverage, int(favorite_id)).get()

                if query:
                    if favorite_bev:
                        query.favorites.push(favorite_bev)
                    self.response.status = 200
                    self.response.write(json.dumps(query.favorites))
                else:
                    new_user = db_defs.User()
                    new_user.email = user_email
                    new_user.favorites = []
                    if favorite_bev:
                        query.favorites.push(favorite_bev)
                    key = new_user.put()
                    if key:

                        self.response.status = 200
                        self.response.write(json.dumps(new_user.favorites))

            except crypt.AppIdentityError:
                # Invalid token
                self.response.status = 401  # bad request
                self.response.message = "Unauthorized, invalid token"
        else:
            self.response.status = 401
            self.response.message = "Unauthorized, no token sent"

        return

