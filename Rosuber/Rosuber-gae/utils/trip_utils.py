import logging

from google.appengine.api import mail
from google.appengine.ext import ndb

from models import Trip
from utils import date_utils


def get_parent_key_from_username(username):
    return ndb.Key("Entity", username)

def get_parent_key(username):
    return get_parent_key_from_username(username)


def get_trips_from_account_info(account_info):
    parent_key = get_parent_key(account_info.rose_username)
    trips = Trip.query(ancestor=parent_key).order(Trip.pick_up_time).fetch()
    trip_map ={}
    for trip in trips:
        trip_map[trip.key]=trip
    return trips, trip_map

def get_driver_trips_from_account_info(account_info):
    driver_trips = Trip.query(Trip.driver==account_info.key).order(Trip.pick_up_time).fetch()
    return driver_trips;

def get_passenger_trips_from_account_info(account_info):
    parent_key = get_parent_key(account_info.rose_username)
    passenger_trips = Trip.query().filter(Trip.passengers.IN([account_info.key])).order(Trip.passengers, Trip.pick_up_time).fetch()
    return passenger_trips

def get_need_driver_trip():
    need_driver_trips_query = Trip.query().filter(ndb.AND(Trip.driver==None, Trip.is_available==True))
    need_driver_trips = need_driver_trips_query.order(Trip.driver, Trip.pick_up_time).fetch()
    return need_driver_trips

def get_need_passenger_trip():
    need_passenger_trips_query = Trip.query().filter(ndb.AND(Trip.is_available==True, Trip.driver!=None))
    need_passenger_trips = need_passenger_trips_query.order(Trip.driver, Trip.pick_up_time).fetch()
    return need_passenger_trips
    
def send_email(email, account_info, trip_origin, trip_destination, trip_time, send_to_other, leave_trip, create_trip):    
    sender_address = "no-reply@wangf-fengy2-rosuber.appspotmail.com"
        
    body = "Hi, NAME! Thanks for choosing Rosuber! You have joined the trip from ORIGIN to DEST on TIME. Please visit www.rosuber.com for more detail of your trip."
    if send_to_other:
        body = "Hi, NAME!  Your trip from ORIGIN to DEST on TIME has changed. Please visit www.rosuber.com for more detail."
    if leave_trip:
        body = "Hi, NAME! Thanks for choosing Rosuber! You have left the trip from ORIGIN to DEST on TIME. Please visit www.rosuber.com if you want to join more trips."
    if create_trip:
        body = "Hi, NAME! Thanks for choosing Rosuber! You have created a trip from ORIGIN to DEST on TIME. Please visit www.rosuber.com for more detail of your trip."

    
    if account_info.nickname:
        body = body.replace("NAME", account_info.nickname)
    else:
        body = body.replace("NAME", account_info.first_name + " " + account_info.last_name)
    body = body.replace("ORIGIN", trip_origin)
    body = body.replace("DEST", trip_destination)
    body = body.replace("TIME", date_utils.date_time_display_format(trip_time, "US/Eastern"))
    logging.info(body) 
      
    try:
        subject_text="Trip Confirmation"
        if leave_trip:
            subject_text = "Trip Cancellation"
        if send_to_other:
            subject_text = "Your Trip Has Changed"
        message = mail.EmailMessage(sender=sender_address, subject=subject_text)
        message.to = "<" + account_info.email + ">"
        message.body = body
        message.send()
        logging.info("The email sent to " + email)
    except:
        logging.error("The email did not send! Avoid the retry")
        
        
        
        
        