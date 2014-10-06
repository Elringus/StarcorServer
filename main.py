import webapp2
import json
from google.appengine.ext import ndb


class Player(ndb.Model):
    login = ndb.StringProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    exp = ndb.FloatProperty()
    last_event_time = ndb.StringProperty()
    battle_rating = ndb.IntegerProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')


class Auth(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'auth': 'OK' if player is not None else 'FAIL'})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class Level(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'level': player.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.level = int(json.loads(self.request.body)['level'])
        player.put()


class Exp(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'exp': player.exp})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.exp = float(json.loads(self.request.body)['exp'])
        player.put()


class LastEventTime(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'last_event_time': player.last_event_time})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.last_event_time = str(json.loads(self.request.body)['last_event_time'])
        player.put()


class BattleRating(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'battle-rating': player.battle_rating})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.battle_rating = int(json.loads(self.request.body)['battle_rating'])
        player.put()


def get_player(request):
    return Player.query(Player.login == request.get('login')).get()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', Auth),
    ('/level', Level),
    ('/exp', Exp),
    ('/last_event_time', LastEventTime),
    ('/battle_rating', BattleRating),
], debug=True)
