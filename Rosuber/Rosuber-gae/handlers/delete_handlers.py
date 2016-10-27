from google.appengine.ext import ndb
import webapp2
from handlers import base_handlers


class DeleteTripAction(base_handlers.BaseAction):
    def post(self):
        trip_key = ndb.Key(urlsafe=self.request.get('trip_to_delete_key'))
        trip_key.delete()
        self.redirect("/trip-history")