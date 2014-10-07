import webapp2
import json
from google.appengine.ext import ndb


class Player(ndb.Model):
    last_event_time = ndb.StringProperty()

    # player profile
    login = ndb.StringProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    exp = ndb.FloatProperty()
    battle_rating = ndb.IntegerProperty()

    # resources
    gold = ndb.IntegerProperty()
    metal = ndb.IntegerProperty()
    lumber = ndb.IntegerProperty()
    magick = ndb.IntegerProperty()

    # ships
    ships = ndb.JsonProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')


class Auth(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'auth': 'OK' if player is not None else 'FAIL'})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


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


#region PLAYER_PROFILE
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


class BattleRating(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'battle_rating': player.battle_rating})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.battle_rating = int(json.loads(self.request.body)['battle_rating'])
        player.put()
#endregion


#region RESOURCES
class Gold(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'gold': player.gold})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.gold = int(json.loads(self.request.body)['gold'])
        player.put()


class Metal(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'metal': player.metal})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.metal = int(json.loads(self.request.body)['metal'])
        player.put()


class Lumber(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'lumber': player.lumber})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.lumber = int(json.loads(self.request.body)['lumber'])
        player.put()


class Magick(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps({'magick': player.magick})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.magick = int(json.loads(self.request.body)['magick'])
        player.put()
#endregion


#region SHIPS
class Ships(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps(player.ships)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.ships = json.loads(self.request.body)
        player.put()
#endregion


def get_player(request):
    return Player.query(Player.login == request.get('login')).get()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', Auth),
    ('/last_event_time', LastEventTime),

    # player profile
    ('/level', Level),
    ('/exp', Exp),
    ('/battle_rating', BattleRating),

    # resources
    ('/gold', Gold),
    ('/metal', Metal),
    ('/lumber', Lumber),
    ('/magick', Magick),

    # ships
    ('/ships', Ships),
], debug=True)
