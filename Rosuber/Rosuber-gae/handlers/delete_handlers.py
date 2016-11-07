import datetime

from google.appengine.ext import ndb
import webapp2

from handlers import base_handlers

    #Actually is LeaveTripAction
class DeleteTripAction(base_handlers.BaseAction):        
    def handle_post(self, email, account_info):
        trip_key = ndb.Key(urlsafe=self.request.get('trip_to_delete_key'))
        trip = trip_key.get()
        account_info_key = account_info.key
        
        #if the user is the driver of the tirp
        if trip.driver == account_info_key:
            trip.driver = None
            if trip.passengers == None:
                trip_key.delete()
            else:
                trip.is_available = True;
                trip.put()
                
        #if the user is one of the passenger of the trip
        else:
            index=trip.passengers.index(account_info_key)
            trip.passengers.pop(index)
            if trip.driver:
                trip.capacity_left +=1;
                if trip.is_available == False:
                    trip.is_available = True
                trip.put()
            else:
                if trip.passengers == None:
                    trip_key.delete()
                else:
                    trip.put()
                    
                    
        today = datetime.datetime.today()
        if today > trip.pick_up_time:
            trip_key.delete()         
       
#         trip_key.delete()
        self.redirect("/trip-history")