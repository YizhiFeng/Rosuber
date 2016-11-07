import datetime
import logging

from google.appengine.api import mail
from google.appengine.ext import ndb
import webapp2

from handlers import base_handlers
from utils import date_utils


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
            else:
                if trip.passengers == []:
                    trip.key.delete()
                else:
                    trip.put()
                    
        self.send_email(email, account_info, trip_origin, trip_destination, trip_time)            
        today = datetime.datetime.today()
        if today > trip.pick_up_time:
            trip_key.delete()         
       
#         trip_key.delete()
        self.redirect("/trip-history")
        
    def send_email(self, email, account_info, trip_origin, trip_destination, trip_time):
        sender_address = "no-reply@wangf-fengy2-rosuber.appspotmail.com"
        logging.info(sender_address)
        
        body = "Hi, NAME! Thanks for choosing Rosuber! You have left the trip from ORIGIN to DEST on TIME. Please visit www.rosuber.com if you want to join more trips."
        if account_info.nickname:
            body = body.replace("NAME", account_info.nickname)
        else:
            body = body.replace("NAME", account_info.first_name + " " + account_info.last_name)
        body = body.replace("ORIGIN", trip_origin)
        body = body.replace("DEST", trip_destination)
        body = body.replace("TIME", date_utils.date_time_display_format(trip_time, "US/Eastern"))
        logging.info(body) 
          
        try:
            message = mail.EmailMessage(sender=sender_address, subject="Trip Cancellation")
            message.to = "<" + account_info.email + ">"
            message.body = body
            message.send()
            logging.info("The email sent to " + email)
        except:
            logging.error("The email did not send! Avoid the retry")
            
            
            
            
