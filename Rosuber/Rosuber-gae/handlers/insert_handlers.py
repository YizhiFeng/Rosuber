import logging

from google.appengine.ext import ndb

from handlers import base_handlers
from models import Trip
from utils import trip_utils


class AccountInfoAction(base_handlers.BaseAction):

    def handle_post(self, email, account_info):
        account_info.rose_username = self.request.get("username")
        account_info.first_name = self.request.get("real_first_name")
        account_info.last_name = self.request.get("real_last_name")
        account_info.phone = self.request.get("phone_number")
        account_info.email = email
        account_info.nickname = self.request.get("nickname")
        account_info.put()
        self.redirect("/profile")
        
class InsertTripAction(base_handlers.BaseAction):
    
    def handle_post(self, email, account_info):
        if self.request.get("trip_entity_key"):
#             trip_key = ndb.Key()
            trip = self.request.get("trip_entity_key").get()
        else:
            trip = Trip(parent=trip_utils.get_parent_key_from_username(account_info.rose_username))
#         trip.driver = self.request.get("")
#         trip.passengers = 
        trip.origin = self.request.get("origin")
        trip.destination = self.request.get("destination")
#         trip.pick_up_time = self.request.get("pick_up_time")
        trip.price = self.request.get("price")
        trip.capacity = int(self.request.get("capacity"))
        trip.put()
        self.redirect("/trip")
        
        
        
        
        