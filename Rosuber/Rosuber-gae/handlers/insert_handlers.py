import logging
import user

from google.appengine.api import mail
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
            trip.capacity_left = int(self.request.get("capacity"))
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
        trip.pick_up_time = pick_up_time
        trip.price = self.request.get("price")
        if self.request.get("capacity"):
            trip.capacity_left = int(self.request.get("capacity"))
        else:
            trip.capacity_left = 0;

        trip.put()
        trip_utils.send_email(email, account_info, trip.origin, trip.destination, trip.pick_up_time, False, False, True)
        
        self.redirect("/find-trip")
        
class UpdateTripAction(base_handlers.BaseAction):
    def handle_post(self, email, account_info):
        trip = ndb.Key(urlsafe=self.request.get("trip_to_update_key")).get()
        update = False
        need_driver = False
        need_passenger = False
        account_info_key = account_info.key
        trip_origin = trip.origin
        trip_destination = trip.destination
        trip_time = trip.pick_up_time
        
        
        if trip.driver == None:
            need_driver = True
        if trip.passengers == None or trip.capacity_left!=0 or trip.passengers == []:
            need_passenger = True
        
        user_is_passenger = self.is_passenger(trip.passengers, account_info.key)
        
        #Trip need driver:
        if need_driver:
            if user_is_passenger==False:
                trip.driver = account_info.key
                update = True
                if trip.capacity_left == 0:
                    trip.is_available = False;
            else:
                logging.info("You are already a passenger")
        
        if need_passenger:
            if trip.driver == account_info.key:
                logging.info("You are already a driver")
            else:
                logging.info("become a passenger")
                if user_is_passenger ==False:
                    trip.passengers.append(account_info.key)
                    update = True
                
        #Check if there is need to update this trip
        if update:
            if need_passenger:
                trip.capacity_left = trip.capacity_left-1;
                if trip.capacity_left == 0:
                    trip.is_available =False;
            if need_driver:
                trip_utils.send_email(email, account_info, trip_origin, trip_destination, trip_time, False, False,False)
            else:
                trip_utils.send_email(trip.driver.get().email, trip.driver.get(), trip_origin, trip_destination, trip_time, True, False,False)
            for p in trip.passengers:
                if p == account_info_key:
                    trip_utils.send_email(email, account_info, trip_origin, trip_destination, trip_time, False, False, False)
                else:
                    trip_utils.send_email(p.get().email, p.get(), trip_origin, trip_destination, trip_time, True, False, False)
            trip.put()
        
        self.redirect("/find-trip")
        
    def is_passenger(self,passenger_list, account_info_key):
        for passenger_key in passenger_list:
            if passenger_key == account_info_key:
                return True
        
        return False
    
        
        