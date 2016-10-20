from google.appengine.ext import ndb
from setuptools.ssl_support import is_available



class User(ndb.Model):
    """ Saves a user to the datastore """

    rose_username = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone = ndb.StringProperty(default="")
    email = ndb.StringProperty()
    trips = ndb.StringProperty(repeated=True)


class Trip(ndb.Model):
    """ Save a trip to the datastore"""
    
    driver = ndb.StringProperty()
    passenger = ndb.StringProperty(repeated=True, default="")
    origin = ndb.StringProperty()
    destination = ndb.StringProperty()
    pick_up_time=ndb.DateTimeProperty()
    is_available = ndb.BooleanProperty(default=True)
    price = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
    