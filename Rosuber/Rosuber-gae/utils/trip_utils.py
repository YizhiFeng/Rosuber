from google.appengine.ext import ndb

from models import Trip


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
    passenger_trips = Trip.query(ancestor=parent_key).filter(Trip.passengers.IN([account_info.key])).order(Trip.passengers, Trip.pick_up_time).fetch()
    return passenger_trips

def get_need_driver_trip():
    need_driver_trips_query = Trip.query().filter(ndb.AND(Trip.driver==None, Trip.is_available==True))
    need_driver_trips = need_driver_trips_query.order(Trip.driver, Trip.pick_up_time).fetch()
    return need_driver_trips

def get_need_passenger_trip():
    need_passenger_trips_query = Trip.query().filter(ndb.AND(Trip.is_available==True, Trip.driver!=None))
    need_passenger_trips = need_passenger_trips_query.order(Trip.driver, Trip.pick_up_time).fetch()
    return need_passenger_trips
    