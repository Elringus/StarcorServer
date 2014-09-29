import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
