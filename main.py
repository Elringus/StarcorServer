import webapp2
import json
import model
import logging


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World, this is the starcor server!')


class Auth(webapp2.RequestHandler):
    def get(self):
        player = model.get_player(self.request)
        data = json.dumps({'auth': 'OK' if player is not None else 'FAIL'})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class EventDelta(webapp2.RequestHandler):
    def get(self):
        data = json.dumps({'event_delta': model.get_event_delta(self.request)})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class ResetState(webapp2.RequestHandler):
    def get(self):
        model.reset_state(self.request)


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


class AddShip(webapp2.RequestHandler):
    def get(self):
        model.add_ship(self.request)


class RemoveAllShips(webapp2.RequestHandler):
    def get(self):
        model.remove_all_ships(self.request)


class GetAllShips(webapp2.RequestHandler):
    def get(self):
        ships = model.get_all_ships(self.request)
        data = '['
        for (i, ship) in enumerate(ships):
            data += '{'
            data += '"Type": "%s",' % ship.type
            data += '"Level": "%s",' % ship.level
            data += '"Count": "%s"' % ship.count
            data += '},'
        data += ']'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)
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


class AddBuilding(webapp2.RequestHandler):
    def get(self):
        model.add_building(self.request)


class RemoveAllBuildings(webapp2.RequestHandler):
    def get(self):
        model.remove_all_buildings(self.request)


class GetAllBuildings(webapp2.RequestHandler):
    def get(self):
        buildings = model.get_all_buildings(self.request)
        data = '['
        for (i, building) in enumerate(buildings):
            data += '{'
            data += '"Type": "%s",' % building.type
            data += '"Built": "%s",' % building.built
            data += '"Level": "%s",' % building.level
            data += '"Position": "%s"' % building.position
            data += '},'
        data += ']'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)
#endregion


#region TOWERS
class TowerType(webapp2.RequestHandler):
    def get(self):
        tower = model.get_tower(self.request)
        data = json.dumps({'tower_type': tower.type})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        tower = model.get_tower(self.request)
        tower.type = int(json.loads(self.request.body)['tower_type'])
        tower.put()


class TowerLevel(webapp2.RequestHandler):
    def get(self):
        tower = model.get_tower(self.request)
        data = json.dumps({'tower_level': tower.level})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        tower = model.get_tower(self.request)
        tower.level = int(json.loads(self.request.body)['tower_level'])
        tower.put()


class TowerPosition(webapp2.RequestHandler):
    def get(self):
        tower = model.get_tower(self.request)
        data = json.dumps({'tower_position': tower.position})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        tower = model.get_tower(self.request)
        tower.position = int(json.loads(self.request.body)['tower_position'])
        tower.put()


class TowerCurrentHP(webapp2.RequestHandler):
    def get(self):
        tower = model.get_tower(self.request)
        data = json.dumps({'tower_current_hp': tower.current_hp})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)

    def post(self):
        tower = model.get_tower(self.request)
        tower.current_hp = float(json.loads(self.request.body)['tower_current_hp'])
        tower.put()


class AddTower(webapp2.RequestHandler):
    def get(self):
        model.add_tower(self.request)


class RemoveTower(webapp2.RequestHandler):
    def get(self):
        model.remove_tower(self.request)


class RemoveAllTowers(webapp2.RequestHandler):
    def get(self):
        model.remove_all_towers(self.request)


class GetAllTowers(webapp2.RequestHandler):
    def get(self):
        towers = model.get_all_towers(self.request)
        data = '['
        for (i, tower) in enumerate(towers):
            data += '{'
            data += '"Type": "%s",' % tower.type
            data += '"Level": "%s",' % tower.level
            data += '"Position": "%s",' % tower.position
            data += '"CurrentHP": "%s",' % tower.current_hp
            data += '},'
        data += ']'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)
#endregion


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', Auth),
    ('/event_delta', EventDelta),
    ('/reset_state', ResetState),

    # player profile
    ('/level', Level),
    ('/exp', Exp),
    ('/battle_rating', BattleRating),

    # resources
    ('/gold', Gold),
    ('/lumber', Lumber),
    ('/metal', Metal),
    ('/magick', Magick),

    # ships
    ('/ship_level', ShipLevel),
    ('/ship_count', ShipCount),
    ('/add_ship', AddShip),
    ('/remove_all_ships', RemoveAllShips),
    ('/get_all_ships', GetAllShips),

    # buildings
    ('/building_built', BuildingBuilt),
    ('/building_level', BuildingLevel),
    ('/building_position', BuildingPosition),
    ('/add_building', AddBuilding),
    ('/remove_all_buildings', RemoveAllBuildings),
    ('/get_all_buildings', GetAllBuildings),

    # towers
    ('/tower_type', TowerType),
    ('/tower_level', TowerLevel),
    ('/tower_position', TowerPosition),
    ('/tower_current_hp', TowerCurrentHP),
    ('/add_tower', AddTower),
    ('/remove_tower', RemoveTower),
    ('/remove_all_towers', RemoveAllTowers),
    ('/get_all_towers', GetAllTowers),
], debug=True)