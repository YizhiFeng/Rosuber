import logging

from google.appengine.ext import ndb
from models import AccountInfo


# Different helper methods to get the parent key.
def get_parent_key_from_username(username):
  return ndb.Key("Entity", username)

def get_parent_key(username):
  return get_parent_key_from_username(username)



# Different helper methods to get the account_info.
def get_account_info_from_username(username):
  """Gets the one and only AccountInfo object for this email. Returns None if AccountInfo object doesn't exist""" 
  parent_key = get_parent_key_from_username(username)
  return AccountInfo.get_by_id(username, parent=parent_key)
  
  
def get_account_info(user_info):
  """Gets the one and only AccountInfo object for this user.  Creates a new AccountInfo object if none exist."""
  username = user_info["username"]
  account_info = get_account_info_from_username(username)
#   account_info.rose_username = username
#   logging.info(username)
#   logging.info(account_info)
  
  if not account_info:
      parent_key = get_parent_key(username)
      logging.info("Creating a new AccountInfo for new user " + username)
      account_info = AccountInfo(parent=parent_key, id=username)
      account_info.put()
  account_info.rose_username = username
  account_info.email = user_info["email"]
  name = user_info["name"].split(" ")
  account_info.first_name = name[0]
  account_info.last_name = name[1]
  return account_info


# def get_account_info_from_sid(account_sid):
#   """Gets the account info for a given Twilio account sid"""
# #   return AccountInfo.query(AccountInfo.twilio_sid == account_sid).fetch(1)[0]
#   return AccountInfo.query(AccountInfo.twilio_sid == account_sid).get()
  
