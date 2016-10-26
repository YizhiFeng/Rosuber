from google.appengine.ext import ndb



class AccountInfo(ndb.Model):
    """ Saves a user to the datastore """

    rose_username = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone = ndb.StringProperty(default="")
    email = ndb.StringProperty()
    nickname = ndb.StringProperty(default="")


class Trip(ndb.Model):
    """ Save a trip to the datastore"""
    
    driver = ndb.KeyProperty(kind=AccountInfo)
    passengers = ndb.KeyProperty(repeated=True, kind=AccountInfo)
    origin = ndb.StringProperty(default="")
    destination = ndb.StringProperty(default="")
    pick_up_time=ndb.DateTimeProperty()
    is_available = ndb.BooleanProperty(default=True)
    price = ndb.StringProperty(default="0")
    capacity = ndb.IntegerProperty()
    