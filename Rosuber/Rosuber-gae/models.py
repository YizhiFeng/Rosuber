from google.appengine.ext import ndb



class AccountInfo(ndb.Model):
    """ Saves a user to the datastore """

    rose_username = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone = ndb.StringProperty(default="")
    email = ndb.StringProperty()
    nickname = ndb.StringProperty()


class Trip(ndb.Model):
    """ Save a trip to the datastore"""
    
    driver = ndb.KeyProperty()
    passengers = ndb.KeyProperty(repeated=True)
    origin = ndb.StringProperty()
    destination = ndb.StringProperty()
    pick_up_time=ndb.DateTimeProperty()
    is_available = ndb.BooleanProperty(default=True)
    price = ndb.StringProperty()
    capacity = ndb.IntegerProperty()
    