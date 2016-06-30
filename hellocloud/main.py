import webapp2
import time


class MainHandler(webapp2.RequestHandler):
    def get(self):
        cur_time = time.gmtime()
        self.response.write('Current Coordinated Universal Time is: ')
        self.response.write(str(cur_time.tm_hour) + 'hr ' + str(cur_time.tm_min) + 'min ' + str(cur_time.tm_sec) + 'sec')
    
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
