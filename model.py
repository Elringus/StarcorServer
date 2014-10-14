from google.appengine.ext import ndb
import datetime


#region PLAYER
class Player(ndb.Model):
    last_event = ndb.DateTimeProperty(default=datetime.datetime.now())

    # player profile
    login = ndb.StringProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    exp = ndb.FloatProperty()
    battle_rating = ndb.IntegerProperty()
    shield_time = ndb.FloatProperty()

    # resources
    gold = ndb.IntegerProperty()
    lumber = ndb.IntegerProperty()
    metal = ndb.IntegerProperty()
    magick = ndb.IntegerProperty()
    platinum = ndb.IntegerProperty()


def get_player(request):
    return Player.query(Player.login == request.get('login')).get()


def get_event_delta(request):
    player = get_player(request)
    now = datetime.datetime.now()
    last = player.last_event
    delta = (now - last).seconds
    player.last_event = now
    player.put()
    return delta


def reset_state(request):
    player = get_player(request)

    player.last_event = datetime.datetime.now()

    player.level = 1
    player.exp = 0
    player.battle_rating = 0
    player.shield_time = 600

    player.gold = 500
    player.lumber = 100
    player.metal = 100
    player.magick = 50
    player.platinum = 7

    player.put()

    remove_all_ships(request)
    Ship(parent=player.key, type=0, count=15).put()
    Ship(parent=player.key, type=1, count=10).put()

    remove_all_buildings(request)
    Building(parent=player.key, type=0, built=True, position=10).put()
    Building(parent=player.key, type=1, built=True, position=15).put()
    Building(parent=player.key, type=2, built=True, position=20).put()
    for i in range(3, 16):
        Building(parent=player.key, type=i).put()

    remove_all_towers(request)
    Tower(parent=player.key, type=0, position=11).put()
    Tower(parent=player.key, type=0, position=12).put()
    Tower(parent=player.key, type=0, position=13).put()
    Tower(parent=player.key, type=1, position=25).put()
#endregion


#region SHIP
class Ship(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    count = ndb.IntegerProperty(default=0)


def get_ship(request):
    return Ship.query(ancestor=get_player(request).key).filter(Ship.type == int(request.get('type'))).get()


def add_ship(request):
    if get_ship(request) is not None:
        return
    Ship(parent=get_player(request).key, type=int(request.get('type'))).put()


def remove_all_ships(request):
    ndb.delete_multi(Ship.query(ancestor=get_player(request).key).fetch(keys_only=True))


def get_all_ships(request):
    return Ship.query(ancestor=get_player(request).key).fetch()
#endregion


#region BUILDING
class Building(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    built = ndb.BooleanProperty(default=False)
    level = ndb.IntegerProperty(default=1)
    position = ndb.IntegerProperty(default=0)


def get_building(request):
    return Building.query(ancestor=get_player(request).key).filter(Building.type == int(request.get('type'))).get()


def add_building(request):
    if get_building(request) is not None:
        return
    Building(parent=get_player(request).key, type=int(request.get('type'))).put()


def remove_all_buildings(request):
    ndb.delete_multi(Building.query(ancestor=get_player(request).key).fetch(keys_only=True))


def get_all_buildings(request):
    return Building.query(ancestor=get_player(request).key).fetch()
#endregion


#region TOWER
class Tower(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    position = ndb.IntegerProperty(default=0)
    current_hp = ndb.FloatProperty(default=1)


def get_tower(request):
    return Tower.query(ancestor=get_player(request).key).filter(Tower.position == int(request.get('position'))).get()


def add_tower(request):
    if get_tower(request) is not None:
        return
    Tower(parent=get_player(request).key, type=int(request.get('type')), position=int(request.get('position'))).put()


def remove_tower(request):
    get_tower(request).key.delete()


def remove_all_towers(request):
    ndb.delete_multi(Tower.query(ancestor=get_player(request).key).fetch(keys_only=True))


def get_all_towers(request):
    return Tower.query(ancestor=get_player(request).key).fetch()
#endregion
