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

def get_driver_trips_from_username(account_info):
    pass