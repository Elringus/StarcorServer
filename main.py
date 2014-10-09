import webapp2
import json
import model


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')


class Auth(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'auth': 'OK' if player is not None else 'FAIL'})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class LastEventTime(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'last_event_time': player.last_event_time})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.last_event_time = str(json.loads(self.request.body)['last_event_time'])
        player.put()


#region PLAYER_PROFILE
class Level(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'level': player.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.level = int(json.loads(self.request.body)['level'])
        player.put()


class Exp(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'exp': player.exp})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.exp = float(json.loads(self.request.body)['exp'])
        player.put()


class BattleRating(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'battle_rating': player.battle_rating})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.battle_rating = int(json.loads(self.request.body)['battle_rating'])
        player.put()
#endregion


#region RESOURCES
class Gold(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'gold': player.gold})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.gold = int(json.loads(self.request.body)['gold'])
        player.put()


class Metal(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'metal': player.metal})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.metal = int(json.loads(self.request.body)['metal'])
        player.put()


class Lumber(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'lumber': player.lumber})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.lumber = int(json.loads(self.request.body)['lumber'])
        player.put()


class Magick(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'magick': player.magick})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        player = model.get_player(self.request)
        player.magick = int(json.loads(self.request.body)['magick'])
        player.put()
#endregion


#region SHIPS
class ShipLevel(webapp2.RequestHandler):
    def get(self):
        ship = model.get_ship(self.request)
        data = json.dumps({'ship_level': ship.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        ship = model.get_ship(self.request)
        ship.level = int(json.loads(self.request.body)['ship_level'])
        ship.put()


class ShipCount(webapp2.RequestHandler):
    def get(self):
        ship = model.get_ship(self.request)
        data = json.dumps({'ship_count': ship.count})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        ship = model.get_ship(self.request)
        ship.count = int(json.loads(self.request.body)['ship_count'])
        ship.put()
#endregion


#region BUILDINGS
class BuildingBuilt(webapp2.RequestHandler):
    def get(self):
        building = model.get_building(self.request)
        data = json.dumps({'building_built': building.built})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        building = model.get_building(self.request)
        building.built = json.loads(self.request.body)['building_built'] == 'True'
        building.put()


class BuildingLevel(webapp2.RequestHandler):
    def get(self):
        building = model.get_building(self.request)
        data = json.dumps({'building_level': building.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        building = model.get_building(self.request)
        building.level = int(json.loads(self.request.body)['building_level'])
        building.put()


class BuildingPosition(webapp2.RequestHandler):
    def get(self):
        building = model.get_building(self.request)
        data = json.dumps({'building_position': building.position})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        building = model.get_building(self.request)
        building.position = int(json.loads(self.request.body)['building_position'])
        building.put()
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
    ('/building_built', BuildingBuilt),
    ('/building_level', BuildingLevel),
    ('/building_position', BuildingPosition),
], debug=True)