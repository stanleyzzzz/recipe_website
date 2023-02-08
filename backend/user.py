'''
Implementation of User related functions
'''

from error import InputError
from json import dumps
import psycopg2

from database import is_admin, get_user_dict, get_user_dict_by_firebase
from connection import get_conn

def user_registration(username, first_name, last_name, email, firebase_id = None):

    is_admin, is_banned = False, False

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    usernames = cur.fetchall()
    
    for curr_username in usernames:
        if username == curr_username[0]:
            cur.close()
            conn.close()
            raise InputError(description='username already in use')
        
    cur.execute("INSERT INTO users (username, first_name, last_name, email, is_admin, is_banned, firebase_id)\
                 VALUES (%s, %s, %s, %s, %s, %s, %s) \
                 RETURNING user_id",
                 (username, first_name, last_name, email, is_admin, is_banned, firebase_id))
    user_id = cur.fetchone()[0]
    if user_id == 1:
        cur.execute(f"UPDATE users SET is_admin = True WHERE user_id = 1")

    conn.commit()
    cur.close()
    conn.close()

    return dumps({
        'user_id': user_id,
    })

def user_dashboard(firebase_id):
    return dumps(get_user_dict_by_firebase(firebase_id))
    
def user_update(user_id, username, first_name, last_name):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("UPDATE users SET username = %s WHERE user_id = %s", [username, user_id])
    cur.execute("UPDATE users SET first_name = %s WHERE user_id = %s", [first_name, user_id])
    cur.execute("UPDATE users SET last_name = %s WHERE user_id = %s", [last_name, user_id])

    conn.commit()
    cur.close()
    conn.close()
    
    return dumps({
        'user_id': user_id,
    })

def list_all_users(requesting_id):

    if not is_admin(requesting_id):
        return dumps({
            'users': []
        })
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    user_ids = cur.fetchall()

    users = []
    for user_id in user_ids:
        user_id = user_id[0]
        users.append(get_user_dict(user_id))
    return dumps({
        'users': users
    })

