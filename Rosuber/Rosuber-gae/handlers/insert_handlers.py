import logging
import user

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Trip
from utils import trip_utils, date_utils, account_utils


class AccountInfoAction(base_handlers.BaseAction):

    def handle_post(self, email, account_info):
        account_info.rose_username = self.request.get("username")
        account_info.first_name = self.request.get("real_first_name")
        account_info.last_name = self.request.get("real_last_name")
        account_info.phone = self.request.get("phone_number")
        account_info.email = email
        account_info.nickname = self.request.get("nickname")
        account_info.put()
        self.redirect("/homepage")
        
class InsertTripAction(base_handlers.BaseAction):
    
    def handle_post(self, email, account_info):
        if self.request.get("trip_entity_key"):
            trip = self.request.get("trip_entity_key").get()
        else:
            trip = Trip(parent=trip_utils.get_parent_key_from_username(account_info.rose_username))
        
        if self.request.get("role_radio_group") == "driver":
            trip.driver = account_info.key
        elif self.request.get("role_radio_group") == "passenger":
            trip.passengers.append(account_info.key)   
        else:
            raise Exception("wrong value")
        
        trip.origin = self.request.get("origin")
        trip.destination = self.request.get("destination")
        pick_up_time= date_utils.get_utc_datetime_from_user_input(account_info.time_zone,
                                                                  self.request.get("pick_up_time"))
        trip.pick_up_time =pick_up_time
        trip.price = self.request.get("price")
        if self.request.get("capacity"):
            trip.capacity_left = int(self.request.get("capacity"))
        else:
            trip.capacity_left = 1;
        
        trip.put()
        self.redirect("/find-trip")
        
class UpdateTripAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        trip = ndb.Key(urlsafe=self.request.get("trip_to_update_key")).get()
        
        if trip.driver:
            trip.passengers.append(account_info.key)
        if trip.passengers:
            trip.driver = account_info.key
        trip.capacity_left = trip.capacity_left-1;
        trip.put()
        self.redirect("/find-trip")
        
        
        
        