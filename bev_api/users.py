import webapp2
from oauth2client import client, crypt


class User(webapp2.RequestHandler):

    def post(self):
        client_id = "957738399987-9epk0j4jne0mgm829q0mhh5sec3cqbhd.apps.googleusercontent.com"

        if 'application/json' not in self.request.accept:
            self.response.status = 400  # bad request
            self.response.status_message = "Invalid Request: This API only supports JSON"
            return

        token = self.request.get('token', default_value=None)

        if token:
            try:
                idinfo = client.verify_id_token(token, client_id)
                self.response.status = 200
                self.response.message = "User authenticated"
            except crypt.AppIdentityError:
                # Invalid token
                self.response.status = 401  # bad request
                self.response.status.message = "Unauthorized, invalid token"

        return