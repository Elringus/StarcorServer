import webapp2
import json
from google.appengine.ext import ndb


class Player(ndb.Model):
    login = ndb.StringProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    exp = ndb.FloatProperty(default=0.1)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')


class Auth(webapp2.RequestHandler):
    def get(self):
        player = Player.query(Player.login == self.request.get('login')).get()
        data = json.dumps({'Auth': 'OK' if player is not None else 'FAIL'})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class Level(webapp2.RequestHandler):
    def get(self):
        player = Player.query(Player.login == self.request.get('login')).get()
        data = json.dumps({'Level': player.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = Player.query(Player.login == self.request.get('login')).get()
        player.level = int(self.request.get('level'))
        player.put()


class Exp(webapp2.RequestHandler):
    def get(self):
        player = Player.query(Player.login == self.request.get('login')).get()
        data = json.dumps({'Exp': player.exp})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = Player.query(Player.login == self.request.get('login')).get()
        player.exp = float(self.request.get('exp'))
        player.put()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', Auth),
    ('/level', Level),
    ('/exp', Exp)
], debug=True)
