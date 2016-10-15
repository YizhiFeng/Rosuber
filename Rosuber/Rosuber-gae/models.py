from google.appengine.ext import ndb



class MovieQuote(ndb.Model):
    """ Saves a quote from a movie to the datastore """

    # Examples of some different property types.
    quote = ndb.StringProperty()
    movie = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)


