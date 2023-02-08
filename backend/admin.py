'''
Implementation of Admin related functions
'''

from pickle import TRUE
from error import InputError
from json import dumps
from database import *
import psycopg2

def admin_ban_user(requesting_user_id, ban_user_id):
    if is_admin(requesting_user_id) is True:
        ban_user(ban_user_id)

def admin_unban_user(requesting_user_id, unban_user_id):
    if is_admin(requesting_user_id) is True:
        unban_user(unban_user_id)
