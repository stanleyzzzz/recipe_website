from pickle import NONE
from database import *
from unittest import TestCase
from error import InputError
from server import setup_server
from user import user_registration, user_dashboard, user_update
import pytest


def test_database():
    setup_server()
    launch_tables()

'''TESTING USER DATABASE FUNCTIONS'''

def test_adding_user():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': False, 'email': None, 'firebase_id': '1'}
    assert get_user_dict_by_firebase('1') == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': False, 'email': None, 'firebase_id': '1'}

def test_getting_user_id():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    assert get_user_id('ZAIDON') == 1

def test_adding_multiple_user():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    add_user('Sammya', "Sim", "Tu", firebase_id = '2')
    assert get_user_dict(2) == {'user_id': 2, 'is_admin': False, 'first_name': 'Sim', 'last_name': 'Tu', 'username': 'Sammya', 'is_banned': False, 'email': None, 'firebase_id': '2'}
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': False, 'email': None, 'firebase_id': '1'}
    assert get_user_id("Sammya") == 2
    assert get_user_id("ZAIDON") == 1

def test_adding_admin():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1', is_admin= True)
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': True, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': False, 'email': None, 'firebase_id': '1'}

def test_adding_banned():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1', is_banned= True)
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': True, 'email': None, 'firebase_id': '1'}

def test_adding_mix_of_users():
    reset_users()
    add_user('user_1', "first1", "1", firebase_id = '1', is_admin= True)
    add_user('user_2', "first2", "2", firebase_id = '2', is_admin= True)
    add_user('user_3', "first3", "3", firebase_id = '3', is_banned= True)
    add_user('user_4', "first4", "4", firebase_id = '4', is_banned= True)
    add_user('user_5', "first5", "5", firebase_id = '5')
    add_user('user_6', "first6", "6", firebase_id = '6')

    user_id1 = get_user_id('user_1')
    user_id2 = get_user_id('user_2')
    user_id3 = get_user_id('user_3')
    user_id4 = get_user_id('user_4')
    user_id5 = get_user_id('user_5')
    user_id6 = get_user_id('user_6')

    assert get_user_dict(user_id1) == {'user_id': user_id1, 'is_admin': True, 'first_name': 'first1', 'last_name': '1', 'username': 'user_1', 'is_banned': False, 'email': None, 'firebase_id': '1'}
    assert get_user_dict(user_id2) == {'user_id': user_id2, 'is_admin': True, 'first_name': 'first2', 'last_name': '2', 'username': 'user_2', 'is_banned': False, 'email': None, 'firebase_id': '2'}
    assert get_user_dict(user_id3) == {'user_id': user_id3, 'is_admin': False, 'first_name': 'first3', 'last_name': '3', 'username': 'user_3', 'is_banned': True, 'email': None, 'firebase_id': '3'}
    assert get_user_dict(user_id4) == {'user_id': user_id4, 'is_admin': False, 'first_name': 'first4', 'last_name': '4', 'username': 'user_4', 'is_banned': True, 'email': None, 'firebase_id': '4'}
    assert get_user_dict(user_id5) == {'user_id': user_id5, 'is_admin': False, 'first_name': 'first5', 'last_name': '5', 'username': 'user_5', 'is_banned': False, 'email': None, 'firebase_id': '5'}
    assert get_user_dict(user_id6) == {'user_id': user_id6, 'is_admin': False, 'first_name': 'first6', 'last_name': '6', 'username': 'user_6', 'is_banned': False, 'email': None, 'firebase_id': '6'}

def test_edit_username():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    edit_username(get_user_id('ZAIDON'), 'GAIN')
    assert get_user_dict(get_user_id('GAIN')) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'GAIN', 'is_banned': False, 'email': None, 'firebase_id': '1'}

def test_delete_user():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    delete_user(user_id)
    assert get_user_dict(user_id) == None
    
def test_isadmin():
    reset_users()
    add_user('user_1', "first1", "1", firebase_id = '1', is_admin= True)
    user_id1 = get_user_id('user_1')
    assert is_admin(user_id1)

def test_banning_user():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    ban_user(user_id)
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': True, 'email': None, 'firebase_id': '1'}

def test_unbanning_user():
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1', is_banned= True)
    user_id = get_user_id('ZAIDON')
    unban_user(user_id)
    assert get_user_dict(1) == {'user_id': 1, 'is_admin': False, 'first_name': 'Zain', 'last_name': 'Wu', 'username': 'ZAIDON', 'is_banned': False, 'email': None, 'firebase_id': '1'}

'''TESTING RECIPE DATABASE FUNCTIONS'''

def test_add_recipe_db():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

def test_removing_recipe():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    remove_recipe(1)
    assert get_recipe(1) == None

def test_edit_recipe():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    edit_recipe_method(1, "Second Method")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'Second Method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

def test_edit_recipe_rating():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    edit_recipe_rating(1, 5)

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 5, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

def test_edit_no_ratings():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    edit_recipe_no_reviews(1, 5)

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 5, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

'''TESTING REVIEW TABLE FUNCTIONS'''
def test_add_review():
    reset_recipes()
    reset_users()
    reset_reviews()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    add_review(1 , 1, "Testing", 4)
    assert get_review_from_recipe_id(1) == [{'review_id': 1, 'user_id': '1', 'recipe_id': 1, 'rating': 4, 'comment': 'Testing', 'username': 'ZAIDON'}]


def test_add_multiple_reviews():
    reset_recipes()
    reset_users()
    reset_reviews()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    add_user('SAMDON', "Sam", "Wu", firebase_id = '2')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    add_review(1 , 1, "Testing", 4)
    add_review(1 , 1, "Testing1", 3)
    assert get_review_from_recipe_id(1) == [{'review_id': 1, 'user_id': '1', 'recipe_id': 1, 'rating': 4, 'comment': 'Testing', 'username': 'ZAIDON'},
                                            {'review_id': 2, 'user_id': '1', 'recipe_id': 1, 'rating': 3, 'comment': 'Testing1', 'username': 'ZAIDON'}]

def test_edit_reviews():
    reset_recipes()
    reset_users()
    reset_reviews()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    add_review(1 , 1, "Testing", 4)
    edit_comment(1, "Edited")
    assert get_review_from_recipe_id(1) == [{'review_id': 1, 'user_id': '1', 'recipe_id': 1, 'rating': 4, 'comment': 'Edited', 'username': 'ZAIDON'}]

def test_rm_reviews():
    reset_recipes()
    reset_users()
    reset_reviews()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    add_review(1 , 1, "Testing", 4)
    delete_review(1)
    assert get_review_from_review_id(1) == []
    assert get_review_from_recipe_id(1) == []

'''TESTING INGREDIENT TABLE FUNCTIONS'''
def test_add_ingredients():
    reset_ingredients()
    id = add_ingredient('Cucumber')
    assert get_ingredient(id) == 'Cucumber'

def test_add_multiple_ingredients():
    reset_ingredients()
    id = add_ingredient('Cucumber')
    id2 = add_ingredient('Capsicum')
    id3 = add_ingredient('Thyme')

    assert get_ingredient(id) == 'Cucumber'
    assert get_ingredient(id2) == 'Capsicum'
    assert get_ingredient(id3) == 'Thyme'


'''TESTING RECIPE INGREDIENT TABLE FUNCTIONS'''
def test_add_recipe_ingredients():
    reset_all_tables()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    recipe_id = add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")
    ingredient_id = add_ingredient('Apple')
    add_recipe_ingredients(ingredient_id, recipe_id, '20')
    assert get_recipes_by_ingredients(ingredient_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '20'}]
    assert get_recipes_ingredients(recipe_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '20'}]
    assert get_ingredient(get_recipes_by_ingredients(recipe_id)[0]['ingredient_id']) == 'Apple'


def test_multiple_recipe_ingredients():
    reset_all_tables()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    recipe_id = add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")
    ingredient_id = add_ingredient('Apple')
    ingredient_id1 = add_ingredient('Pie')
    add_recipe_ingredients(ingredient_id, recipe_id, '20')
    add_recipe_ingredients(ingredient_id1, recipe_id, '1')
    assert get_recipes_by_ingredients(ingredient_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '20'}]
    assert get_recipes_ingredients(recipe_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '20'}, {'ingredient_id': ingredient_id1, 'recipe_id': recipe_id, 'amount': '1'}]
    assert get_ingredient(get_recipes_ingredients(recipe_id)[0]['ingredient_id']) == 'Apple'
    assert get_ingredient(get_recipes_ingredients(recipe_id)[1]['ingredient_id']) == 'Pie'

    
def test_remove_recipe_ingredeients():
    reset_all_tables()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    recipe_id = add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")
    ingredient_id = add_ingredient('Apple')
    add_recipe_ingredients(ingredient_id, recipe_id, '20')
    remove_recipe_ingredients(ingredient_id, recipe_id)
    assert get_recipes_by_ingredients(ingredient_id) == []
    assert get_recipes_ingredients(recipe_id) == []

def test_update_recipe_ingredients():
    reset_all_tables()
    add_user('ZAIDON', "Zain", "Wu", firebase_id = '1')
    user_id = get_user_id('ZAIDON')
    recipe_id = add_recipe_db(user_id, 12, "This is a method", "thisisimage", "Recipe Title")
    ingredient_id = add_ingredient('Apple')
    add_recipe_ingredients(ingredient_id, recipe_id, '20')
    update_recipe_ingredients_amount(ingredient_id, recipe_id, '1')
    assert get_recipes_by_ingredients(ingredient_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '1'}]
    assert get_recipes_ingredients(recipe_id) == [{'ingredient_id': ingredient_id, 'recipe_id': recipe_id, 'amount': '1'}]
    assert get_ingredient(get_recipes_by_ingredients(recipe_id)[0]['ingredient_id']) == 'Apple'

