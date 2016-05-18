import logging
import time
import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class ReleaseHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Get')
        logging.info('Get request at ' + str(time.strftime("%c")))
        logging.info(self.request)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/release', ReleaseHandler)
], debug=True)
