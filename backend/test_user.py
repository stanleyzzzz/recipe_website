from unittest import TestCase
from error import InputError
from server import setup_server
from user import user_registration, user_dashboard, user_update, list_all_users
import pytest

import json

def test_registration_simple():
    setup_server()
    # output = json.loads(user_registration("'stanleyz'", "'stanley'", "'zhou'"))
    output = json.loads(user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com'))
    user_id = output['user_id']
    assert user_id == 1
    print('test passed')
    
def test_registration_duplicated_user_name():
    setup_server()
    user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com')
    with pytest.raises(InputError):
            user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com')

    print('test passed')

def test_dashboard():
    setup_server()
    user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com', firebase_id= '1')
    output = json.loads(user_dashboard('1'))
    assert output['user_id'] == 1
    assert output['is_admin'] == True
    assert output['first_name'] == 'stanley'
    assert output['last_name'] == 'zhou'
    assert output['username'] == 'stanleyz'
    assert output['is_banned'] == False
    print('test passed')

def test_update():
    setup_server()
    user_registration('pierrel', 'pierre', 'lingat', 'plingat@gmail.com', firebase_id = '1')
    user_update(1, 'stanleyz', 'stanley', 'zhou')
    
    output = json.loads(user_dashboard('1'))
    #print(output)
    assert output['user_id'] == 1
    assert output['is_admin'] == True
    assert output['first_name'] == 'stanley'
    assert output['last_name'] == 'zhou'
    assert output['username'] == 'stanleyz'
    assert output['is_banned'] == False
    print('test passed')

def test_users():
    setup_server()
    user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com', firebase_id = 'idid')
    output = json.loads(list_all_users(requesting_id = 'idid'))['users']
    
    assert output[0] == {'user_id': 1, 'is_admin': True, 'first_name': 'stanley', 'last_name': 'zhou', 'username': 'stanleyz', 'email': 'szhou@gmail.com', 'is_banned': False, 'firebase_id': 'idid'}
    print('test passed')

def test_users_multiple():
    setup_server()
    user_registration('stanleyz', 'stanley', 'zhou', 'szhou@gmail.com', firebase_id = 'idid')
    user_registration('pierrel', 'pierre', 'lingat', 'plingat@gmail.com', firebase_id = 'ididnot')
    output = json.loads(list_all_users(requesting_id='idid'))['users']
    
    assert output[0] == {'user_id': 1, 'is_admin': True, 'first_name': 'stanley', 'last_name': 'zhou', 'username': 'stanleyz', 'email': 'szhou@gmail.com', 'is_banned': False, 'firebase_id': 'idid'}
    assert output[1] == {'user_id': 2, 'is_admin': False, 'first_name': 'pierre', 'last_name': 'lingat', 'username': 'pierrel', 'email': 'plingat@gmail.com', 'is_banned': False, 'firebase_id': 'ididnot'}
    print('test passed')

if __name__ == "__main__":
    
    test_registration_simple()
    test_registration_duplicated_user_name()
    test_dashboard()
    test_update()
    test_users()
    test_users_multiple()