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

    # buildings
    buildings = ndb.JsonProperty()


def get_player(request):
    return Player.query(Player.login == request.get('login')).get()


class Ship(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    count = ndb.IntegerProperty(default=0)


def get_ship(request):
    ship = Ship.query(ancestor=get_player(request).key).filter(Ship.type == int(request.get('type'))).get()
    if ship is None:
        ship = Ship(parent=get_player(request).key, type=int(request.get('type')))
    return ship


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
class ShipLevel(webapp2.RequestHandler):
    def get(self):
        ship = get_ship(self.request)
        data = json.dumps({'ship_level': ship.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        ship = get_ship(self.request)
        ship.level = int(json.loads(self.request.body)['ship_level'])
        ship.put()


class ShipCount(webapp2.RequestHandler):
    def get(self):
        ship = get_ship(self.request)
        data = json.dumps({'ship_count': ship.count})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        ship = get_ship(self.request)
        ship.count = int(json.loads(self.request.body)['ship_count'])
        ship.put()
#endregion


#region BUILDINGS
class Buildings(webapp2.RequestHandler):
    def get(self):
        player = get_player(self.request)
        data = json.dumps(player.buildings)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = get_player(self.request)
        player.buildings = json.loads(self.request.body)
        player.put()
#endregion


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
    ('/ship_level', ShipLevel),
    ('/ship_count', ShipCount),

    # buildings
    ('/buildings', Buildings),
], debug=True)
