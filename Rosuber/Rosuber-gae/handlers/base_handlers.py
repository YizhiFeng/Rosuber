
import json
import user

from google.appengine.api import users
import webapp2
from webapp2_extras import sessions

import main
from utils import account_utils


class Handler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


# Potentially helpful (or not) superclass for *logged in* pages and actions (assumes app.yaml gaurds for login)
### Pages ###
class BaseHandler(Handler): 
  def get(self):
    if "user_info" in self.session:
        self.roseLogin()
    else:    
        self.redirect("/")

  def roseLogin(self):
    template = main.jinja_env.get_template(self.get_template())
    if not "user_info" in self.session:
        raise Exception("No rose user logged in")
    user_info = json.loads(self.session["user_info"])
    email = user_info["email"]
    username = user_info["username"]
    account_info = account_utils.get_account_info(user_info)
    values = {"user_info": user_info,
              "account_info": account_info,
              "user_email": email}
    self.update_values(email, values)  
    self.response.out.write(template.render(values))
    
  def get_page_title(self):
      
      return "Rosuber"
  
  def update_values(self, user, values):
    # Subclasses should override this method to add additional data for the Jinja template.
    pass


  def get_template(self):
    # Subclasses must override this method to set the Jinja template.
    raise Exception("Subclass must implement handle_post!")
    pass





### Actions ###

class BaseAction(BaseHandler):
  """ALL action handlers should inherit from this one."""
  def post(self):
    if "user_info" in self.session:
        user_info = json.loads(self.session["user_info"])
        email = user_info["email"]
    else:
      raise Exception("Missing user!")
    account_info = account_utils.get_account_info(user_info)
    self.handle_post(email,account_info)  # Update what is passed to subclass function as needed


  def get(self):
    self.post()  # Action handlers should not use get requests.


  def handle_post(self, email,account_info):
    # Subclasses must override this method to handle the request.
    raise Exception("Subclass must implement handle_post!")