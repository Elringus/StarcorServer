import logging
import main
import webapp2
import json
import model
import random
import string
from webapp2_extras import auth as wbauth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError


def auth_required(handler):
    """
      Decorator that checks if there's a user associated with the current session.
      Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        au = wbauth.get_auth()
        if not au.get_user_by_session():
            data = json.dumps({'auth': 'FAIL'})
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(data)
        else:
            return handler(self, *args, **kwargs)

    return check_login


class AuthBase(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return wbauth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
          config['webapp2_extras.auth']['user_attributes'].
        :returns
          A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
          The instance of the user model associated to the logged in user.
        """
        user = self.user_info
        return self.user_model.get_by_id(user['user_id']) if user else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


class Signup(AuthBase):
    def post(self):
        login = str(json.loads(self.request.body)['login'])

        if model.get_player(login) is not None:
            data = json.dumps({'result': 'Signup fail: provided login already exists.'})
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(data)
            return

        unique_properties = ['login']
        random_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        self.user_model.create_user(login, unique_properties, login=login,
                                    password_raw=random_password, verified=True)

        data = json.dumps({'result': 'OK', 'password': random_password})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(data)


class Login(AuthBase):
    def post(self):
        login = str(json.loads(self.request.body)[0]['login'])
        password = str(json.loads(self.request.body)[1]['password'])
        # logging.debug("login: " + login + " password: " + password)
        try:
            self.auth.get_user_by_password(login, password, remember=True, save_session=True)
            data = json.dumps({'result': 'OK'})
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(data)
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            data = json.dumps({'result': 'Login fail: %s' % type(e)})
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(data)


class Logout(AuthBase):
    @auth_required
    def get(self):
        self.auth.unset_session()
