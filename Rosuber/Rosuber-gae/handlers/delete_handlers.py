import datetime
import logging

from google.appengine.api import mail
from google.appengine.ext import ndb
import webapp2

from handlers import base_handlers
from utils import date_utils, trip_utils


    # Actually is LeaveTripAction
class DeleteTripAction(base_handlers.BaseAction):        
    def handle_post(self, email, account_info):
        trip_key = ndb.Key(urlsafe=self.request.get('trip_to_delete_key'))
        trip = trip_key.get()
        account_info_key = account_info.key
        trip_origin = trip.origin
        trip_destination = trip.destination
        trip_time = trip.pick_up_time
        
        # if the user is the driver of the tirp
        if trip.driver == account_info_key:
            trip.driver = None
            if trip.passengers == []:
                trip.key.delete()
            else:
                for p in trip.passengers:
                    trip_utils.send_email(p.get().email, p.get(), trip_origin, trip_destination, trip_time, True, False, False)
                trip.put()
                
        # if the user is one of the passenger of the trip
        else:
            index = trip.passengers.index(account_info_key)
            trip.passengers.pop(index)
            
            if trip.driver:
                trip.capacity_left += 1;
                if trip.is_available == False:
                    trip.is_available = True
                trip.put()
                trip_utils.send_email(trip.driver.get().email, trip.driver.get(), trip_origin, trip_destination, trip_time, True, False,False)
                for p in trip.passengers:
                    trip_utils.send_email(p.get().email, p.get(), trip_origin, trip_destination, trip_time, True, False, False)
            else:
                if trip.passengers == []:
                    trip.key.delete()
                else:
                    for p in trip.passengers:
                        trip_utils.send_email(p.get().email, p.get(), trip_origin, trip_destination, trip_time, True, False, False)
                    trip.put()
                    
        trip_utils.send_email(email, account_info, trip_origin, trip_destination, trip_time,False,True, False)            
        today = datetime.datetime.today()
        if today > trip.pick_up_time:
            trip_key.delete()         
       
#         trip_key.delete()
        self.redirect("/trip-history")
            
            
            
            
