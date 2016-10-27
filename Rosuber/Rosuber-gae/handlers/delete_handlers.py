from google.appengine.ext import ndb
import webapp2


class DeleteTripAction(webapp2.RequestHandler):
    def post(self):
        trip_key = ndb.Key(urlsafe=self.request.get('trip_to_delete_key'))
        trip_key.delete()
        self.redirect("/trip-history")