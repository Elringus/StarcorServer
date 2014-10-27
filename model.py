import webapp2_extras.appengine.auth.models
from webapp2_extras import security
from google.appengine.ext import ndb
import datetime
import time
import logging


#region PLAYER
class Player(webapp2_extras.appengine.auth.models.User):
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

    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None


def get_player(login):
    return Player.query(Player.login == login).get()


def get_event_delta(request):
    player = get_player(request.get('login'))
    now = datetime.datetime.now()
    last = player.last_event
    delta = (now - last).seconds
    player.last_event = now
    player.put()
    return delta


def reset_state(request):
    player = get_player(request.get('login'))

    player.last_event = datetime.datetime.now()

    player.level = 1
    player.exp = 0
    player.battle_rating = 0
    player.shield_time = 600

    player.gold = 9999
    player.lumber = 9999
    player.metal = 9999
    player.magick = 9999
    player.platinum = 9999

    player.put()

    remove_all_ships(request)
    Ship(parent=player.key, type=0, count=15).put()
    Ship(parent=player.key, type=1, count=10).put()

    remove_all_buildings(request)
    Building(parent=player.key, type=0, built=True, position=33).put()
    Building(parent=player.key, type=1, built=True, position=3).put()
    Building(parent=player.key, type=2, built=True, position=2).put()
    for i in range(3, 16):
        Building(parent=player.key, type=i).put()

    remove_all_towers(request)
    # Tower(parent=player.key, type=0, position=1).put()
    # Tower(parent=player.key, type=0, position=2).put()
    # Tower(parent=player.key, type=0, position=3).put()
    # Tower(parent=player.key, type=5, position=6).put()
#endregion


#region SHIP
class Ship(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    count = ndb.IntegerProperty(default=0)


def get_ship(request):
    return Ship.query(ancestor=get_player(request.get('login')).key).filter(Ship.type == int(request.get('type'))).get()


def add_ship(request):
    if get_ship(request) is not None:
        return
    Ship(parent=get_player(request.get('login')).key, type=int(request.get('type'))).put()


def remove_all_ships(request):
    ndb.delete_multi(Ship.query(ancestor=get_player(request.get('login')).key).fetch(keys_only=True))


def get_all_ships(request):
    return Ship.query(ancestor=get_player(request.get('login')).key).fetch()
#endregion


#region BUILDING
class Building(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    built = ndb.BooleanProperty(default=False)
    level = ndb.IntegerProperty(default=1)
    position = ndb.IntegerProperty(default=0)


def get_building(request):
    return Building.query(ancestor=get_player(request.get('login')).key).filter(Building.type == int(request.get('type'))).get()


def add_building(request):
    if get_building(request) is not None:
        return
    Building(parent=get_player(request.get('login')).key, type=int(request.get('type'))).put()


def remove_all_buildings(request):
    ndb.delete_multi(Building.query(ancestor=get_player(request.get('login')).key).fetch(keys_only=True))


def get_all_buildings(request):
    return Building.query(ancestor=get_player(request.get('login')).key).fetch()
#endregion


#region TOWER
class Tower(ndb.Model):
    type = ndb.IntegerProperty(required=True)
    level = ndb.IntegerProperty(default=1)
    position = ndb.IntegerProperty(default=0)
    current_hp = ndb.FloatProperty(default=1)


def get_tower(request):
    return Tower.query(ancestor=get_player(request.get('login')).key).filter(Tower.position == int(request.get('position'))).get()


def add_tower(request):
    if get_tower(request) is not None:
        return
    Tower(parent=get_player(request.get('login')).key, type=int(request.get('type')), position=int(request.get('position'))).put()


def remove_tower(request):
    get_tower(request).key.delete()


def remove_all_towers(request):
    ndb.delete_multi(Tower.query(ancestor=get_player(request.get('login')).key).fetch(keys_only=True))


def get_all_towers(request):
    return Tower.query(ancestor=get_player(request.get('login')).key).fetch()
#endregion
