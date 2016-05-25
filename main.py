import webapp2
import one_piece_bot
from timeit import default_timer as timer


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(one_piece_bot.get_status())


class ReleaseHandler(webapp2.RequestHandler):
    def get(self):
        start_time = timer()
        one_piece_bot.check_releases()
        self.response.write("Request completed in " + str((timer() - start_time)) + " seconds.")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/release', ReleaseHandler)
], debug=True)
