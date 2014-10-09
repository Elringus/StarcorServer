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


class Building(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    built = ndb.BooleanProperty(default=False)
    level = ndb.IntegerProperty(default=1)
    position = ndb.IntegerProperty(default=0)


def get_building(request):
    building = Building.query(ancestor=get_player(request).key).filter(Building.type == int(request.get('type'))).get()
    if building is None:
        building = Building(parent=get_player(request).key, type=int(request.get('type')))
    return building