import json
import os

from google.appengine.api import users
import jinja2
import webapp2

from handlers import base_handlers, delete_handlers
from handlers import insert_handlers
from models import Trip
from rosefire import RosefireTokenVerifier
import utils
from utils import trip_utils


# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    # Example of a Jinja filter (useful for formatting data sometimes)
    #   jenv.filters["time_and_date_format"] = date_utils.time_and_date_format
    return jenv

jinja_env = __init_jinja_env()
ROSEFIRE_SECRET = 'omf1cPaSTlhPOTItFIAb'

class HomePage(base_handlers.BaseHandler):
    
#     def update_values(self, email, values):
#         # Subclasses should override this method to add additional data for the Jinja template.
#         

    def get_template(self):
        return "templates/homepage.html"

    def get_page_title(self):
        return "Rosuber"
    
    def update_values(self, account_info, values):
#         values["availabe_trip"]
#         values["trip_history"]
#         values["trips"]
        pass

class LoginPage(base_handlers.BaseHandler):
    def get(self):
        values = {}
        if "user_info" in self.session:
            self.redirect("/homepage")
            return
        template = jinja_env.get_template("templates/login.html")
        values = {"login_url":users.create_login_url("/homepage")}
        self.response.out.write(template.render(values))

class ProfilePage(base_handlers.BaseHandler):
        
    def get_template(self):
        return "templates/profile.html"
    def get_page_title(self):
        return "Rosuber"

class TripHistoryPage(base_handlers.BaseHandler):
    def get_template(self):
        return "templates/trip_history.html"
    def get_page_title(self):
        return "Rosuber"
    def update_values(self, account_info, values):
        values["trip_list"], values["trip_map"]=trip_utils.get_trips_from_account_info(account_info)

class TripPage(base_handlers.BaseHandler):
    def update_values(self, account_info, values):
        values["trip_list"], values["trip_map"]=trip_utils.get_trips_from_account_info(account_info)
        
    def get_template(self):
        return "templates/create_trip.html"
    def get_page_title(self):
        return "Rosuber"

class LoginHandler(base_handlers.BaseHandler):
    def get(self):
        if "user_info" not in self.session:
            token = self.request.get('token')
            auth_data = RosefireTokenVerifier(ROSEFIRE_SECRET).verify(token)
            user_info = {"name": auth_data.name,
                         "username": auth_data.username,
                         "email": auth_data.email,
                         "role": auth_data.group}
            self.session["user_info"] = json.dumps(user_info)
        self.redirect(uri="/")

class LogoutHandler(base_handlers.BaseHandler):
    def get(self):
        del self.session["user_info"]
        self.redirect(uri="/")

config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'somethingsupertopsecret',
}

app = webapp2.WSGIApplication([
    #Page
    ('/', LoginPage),
    ('/homepage', HomePage),
    ('/profile', ProfilePage),
    ('/trip-history', TripHistoryPage),
    ('/trip', TripPage),
    
    #Login/Logout
    ('/rosefire-login', LoginHandler),
    ('/rosefire-logout', LogoutHandler),
    
    
    #Actions - Insert
    ('/account-info-action', insert_handlers.AccountInfoAction),
    ('/insert-trip-action', insert_handlers.InsertTripAction),
    
    #Actions - Delete
    ('/delete-trip-action', delete_handlers.DeleteTripAction)
], config=config, debug=True)
