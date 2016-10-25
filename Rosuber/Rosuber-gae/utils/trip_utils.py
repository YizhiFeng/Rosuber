from models import Trip

def get_parent_key_from_account_info(account_info):
    return account_info.get_key()

def get_parent_key(account_info):
    return get_parent_key_from_account_info(account_info)


def get_trips_from_username(account_info):
    parent_key = get_parent_key(account_info)
    trips = Trip.query(ancestor=parent_key).order(Trip.pick_up_time)

def get_driver_trips_from_username(account_info):
    pass