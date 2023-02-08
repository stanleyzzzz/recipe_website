from pip import main
from database import add_review
from error import InputError
from server import setup_server
from user import user_registration
from recipe import edit_recipe_review, delete_recipe_review, add_recipe_review, add_recipe, delete_recipe, update_recipe, search_recipe_name, get_recipe_by_id, get_recipe_by_user, get_recipe_all, get_ingredients, blacklist_ingredients, whitelist_ingredients, suggest_next_ingredient, frequent_ingredients_without_recipe, get_recipes_by_type, sort_recipes_rating, sort_recipes_no_reviews
from database import get_review_from_recipe_id, reset_recipes, reset_users, add_user, add_recipe_db, get_ingredient_id
from connection import get_conn
import pytest

import json

def test_add_recipe():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

def test_add_recipe2():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id1 = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])
 
    user_registration('stanleyz', "S", "Z", 'szhou@gmil.com', 'id2')
    user_id2 = 2
    image_url = 'https://imgix.theurbanlist.com/content/article/botswana-butchery-steak.jpg?auto=format,compress&w=520&h=390&fit=crop'
    add_recipe('id2', 'Steak', 10, 'The way to cook a steak', image_url, ['beef'])

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id1, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}
    assert get_recipe(2) == {'recipe_id': 2, 'user_id': user_id2, 'ratings': 0, 'prep_time': 10, 'no_reviews': 0, 'method': 'The way to cook a steak', 'image': image_url, 'title': 'Steak', 'type': 'Other'}

def test_add_recipe_ingredient1():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])
    # print(get_ingredients_all())
    # print(get_recipe_ingredients_all())
    assert get_ingredients_all() == [(1, 'beef')]
    assert get_recipe_ingredients_all() == [(1, 1, None)]

def test_add_recipe_ingredient2():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['beef'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])
    add_recipe('id', 'Recipe Title3', 12, 'This is a method', 'thisisimage', ['beef'])

    assert get_ingredients_all() == [(1, 'beef')]
    assert get_recipe_ingredients_all() == [(1, 1, None), (1, 2, None), (1, 3, None)]

def test_add_recipe_ingredient3():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['beef', 'pork', 'chicken'])

    assert get_ingredients_all() == [(1, 'beef'), (2, 'pork'), (3, 'chicken')]
    assert get_recipe_ingredients_all() == [(1, 1, None), (2, 1, None), (3, 1, None)]

def test_add_recipe_ingredient4():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['beef', 'pork', 'chicken'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef', 'pork', 'chicken'])
    add_recipe('id', 'Recipe Title3', 12, 'This is a method', 'thisisimage', ['beef', 'pork', 'chicken'])
    
    assert get_ingredients_all() == [(1, 'beef'), (2, 'pork'), (3, 'chicken')]
    assert get_recipe_ingredients_all() == [(1, 1, None), (2, 1, None), (3, 1, None),
                                            (1, 2, None), (2, 2, None), (3, 2, None),
                                            (1, 3, None), (2, 3, None), (3, 3, None)]

def test_delete_recipe_admin_creator():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}
    delete_recipe(1, 'id')

    # print(get_ingredients_all())
    # print(get_recipe_ingredients_all())

    assert get_recipe(1) == None

def test_delete_recipe_creator():
    setup_server()
    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'idea')
    user_registration('stanleyz', "S", "Z", 'szhou@gmil.com', 'id1')
    creator_user_id = 2

    add_recipe('id1', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])
    assert get_recipe(1) == {'recipe_id': 1, 'user_id': creator_user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    delete_recipe(1, 'idea')
    assert get_recipe(1) == None

def test_delete_recipe_admin():
    setup_server()

    user_registration('ZAIDON', "Zain", "Wu", 'zwu@gmil.com', 'idea')
    user_registration('stanleyz', "S", "Z", 'szhou@gmil.com', 'id1')
    creator_user_id = 2

    add_recipe('id1', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef'])
    assert get_recipe(1) == {'recipe_id': 1, 'user_id': creator_user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other'}

    delete_recipe(1, 'idea')
    assert get_recipe(1) == None

def test_delete_recipe_ingredient():
    setup_server()

    user_registration('stanleyz', "S", "Z", 'szhou@gmil.com', 'idea')
    user_id = 1

    add_recipe('idea', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['beef'])
    add_recipe('idea', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['chicken'])

    delete_recipe(1, 'idea')
    delete_recipe(2, 'idea')
    assert get_ingredients_all() == [(1, 'beef'), (2, 'chicken')]
    assert get_recipe_ingredients_all() == []

def test_update_recipe_1():
    setup_server()

    user_registration('stanleyz', "S", "Z", 'szhou@gmil.com', firebase_id= 'FireID')
    user_id = 1
    add_recipe('FireID', 'Recipe Title1', 12, 'This is a method', 'thisisimage', ['beef'])
    recipe_id = 1
    update_recipe('FireID', recipe_id, 'New Recipe Title', 120, 'New method', 'image')

    assert get_recipe(recipe_id) == {'recipe_id': 1, 'user_id': 1, 'ratings': 0, 'prep_time': 120, 'no_reviews': 0, 'method': 'New method', 'image': 'image', 'title': 'New Recipe Title', 'type': 'Other'}
    
def test_get_recipe_by_id():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'idd')
    user_id = 1
    add_recipe('idd', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe_review('idd', 1, 'good _recipe', 5)
    data = json.loads(get_recipe_by_id(1))['recipe']
    assert data == {'recipe_id': 1, 'user_id': user_id, 'ratings': 5.0, 'prep_time': 12, 'no_reviews': 1, 'method': 'This is a method', 
                                    'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other', 'reviews': [{'review_id': 1, 'user_id': 'idd', 'recipe_id': 1, 'rating': 5, 'comment': 'good _recipe', 'username': 'szhou'}],
                                     'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'}

def test_get_recipe_by_user():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', firebase_id = 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe_review('id', 1, 'good _recipe', 5)
    data = json.loads(get_recipe_by_user('id'))['recipes']

    assert data == [{'recipe_id': 1, 'user_id': 1, 'ratings': 5, 'prep_time': 12, 'no_reviews': 1, 'method': 'This is a method', 'image': 'thisisimage', 
                                'title': 'Recipe Title', 'type': 'Other', 'reviews': [{'review_id': 1, 'user_id': 'id', 'recipe_id': 1, 'rating': 5, 'comment': 'good _recipe', 'username': 'szhou'}], 'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'}]

def test_get_recipe_by_user_2():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', firebase_id='id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 120, 'This is a method 2', 'thisisimage', ['beef'])
    add_recipe_review('id', 1, 'good _recipe', 5)
    data = json.loads(get_recipe_by_user('id'))['recipes']

    assert data == [{'recipe_id': 2, 'user_id': 1, 'ratings': 0.0, 'prep_time': 120, 'no_reviews': 0, 'method': 'This is a method 2', 'image': 'thisisimage',
                     'title': 'Recipe Title2', 'type': 'Other', 'username': 'szhou', 'reviews': [], 'ingredients': ['beef']}, {'recipe_id': 1, 'user_id': 1, 'ratings': 5.0, 
                     'prep_time': 12, 'no_reviews': 1, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other', 'username': 'szhou', 
                     'reviews': [{'review_id': 1, 'user_id': 'id', 'recipe_id': 1, 'rating': 5, 'comment': 'good _recipe', 'username': 'szhou'}], 'ingredients': ['beef', 'chicken', 'pork']}]

def test_get_recipe_all():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe_review('id', 1, 'good _recipe', 5)

    user_registration('szhou2', "szhou2", "szhou2", 'szhou2@gmil.com', 'idea')
    user_id = 2
    add_recipe('idea', 'Recipe Title2', 120, 'This is a method 2', 'thisisimage', ['beef'])
    
    data = json.loads(get_recipe_all())['recipes']
    assert data == [{'recipe_id': 1, 'user_id': 1, 'ratings': 5, 'prep_time': 12, 'no_reviews': 1, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title', 'username': 'szhou',
                     'reviews': [{'review_id': 1, 'user_id': 'id', 'recipe_id': 1, 'rating': 5, 'comment': 'good _recipe', 'username': 'szhou'}], 'ingredients': ['beef', 'chicken', 'pork'], 'type': 'Other'}, 
                    {'recipe_id': 2, 'user_id': 2, 'ratings': 0, 'prep_time': 120, 'no_reviews': 0, 'type': 'Other', 'method': 'This is a method 2', 'image': 'thisisimage', 'title': 'Recipe Title2', 'username': 'szhou2',
                     'reviews': [], 'ingredients': ['beef']}]

def test_ingredients():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    
    ingredients = json.loads(get_ingredients())['ingredients']
    assert ingredients == ['beef', 'chicken', 'pork']

def test_ingredients_2():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com','id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['cucumber', 'spinash', 'pork'])
    
    ingredients = json.loads(get_ingredients())['ingredients']
    assert ingredients == ['beef', 'chicken', 'pork', 'cucumber', 'spinash']

def test_blacklist():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])

    recipes = json.loads(get_recipe_all())['recipes']
    assert blacklist_ingredients(recipes, ['pork']) == []

def test_blacklist_2():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])

    recipes = json.loads(get_recipe_all())['recipes']
    assert blacklist_ingredients(recipes, ['spinach']) == [{'recipe_id': 1, 'user_id': 1, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 
                                                            'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other', 'reviews': [], 'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'}]

def test_blacklist_3():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])

    recipes = json.loads(get_recipe_all())['recipes']
    # print(recipes)
    # print(blacklist_ingredients(recipes, ['beef']))
    assert blacklist_ingredients(recipes, ['beef']) == []

def test_whitelist():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])

    recipes = json.loads(get_recipe_all())['recipes']

    assert whitelist_ingredients(recipes, ['beef']) == [{'recipe_id': 1, 'user_id': 1, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 
                                                            'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other', 'reviews': [], 'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'},
                                                            {'recipe_id': 2, 'user_id': 1, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 
                                                            'image': 'thisisimage', 'title': 'Recipe Title2', 'type': 'Other', 'reviews': [], 'ingredients': ['beef'], 'username': 'szhou'}]

def test_whitelist1():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])

    recipes = json.loads(get_recipe_all())['recipes']

    assert whitelist_ingredients(recipes, ['chicken']) == [{'recipe_id': 1, 'user_id': 1, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 
                                                            'image': 'thisisimage', 'title': 'Recipe Title', 'type': 'Other', 'reviews': [], 'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'}]

def test_whitelist2():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])

    recipes = json.loads(get_recipe_all())['recipes']

    assert whitelist_ingredients(recipes, ['thyme']) == []

def test_frequent_ingredients_without_recipe():

    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    user_id = 1
    add_recipe('id', 'Recipe Title', 12, 'This is a method', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Recipe Title2', 12, 'This is a method', 'thisisimage', ['beef'])

    frequent_ingredients_without_recipe()

    #assert whitelist_ingredients(recipes, ['thyme']) == []

'''
def test_edit_recipe():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu")
    user_id = get_user_id('ZAIDON')
    add_recipe(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title'}

    edit_recipe_method(1, "Second Method")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'Second Method', 'image': 'thisisimage', 'title': 'Recipe Title'}

def test_edit_recipe_rating():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu")
    user_id = get_user_id('ZAIDON')
    add_recipe(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title'}

    edit_recipe_rating(1, 5)

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 5, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title'}

def test_edit_no_ratings():
    reset_recipes()
    reset_users()
    add_user('ZAIDON', "Zain", "Wu")
    user_id = get_user_id('ZAIDON')
    add_recipe(user_id, 12, "This is a method", "thisisimage", "Recipe Title")

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 0, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title'}

    edit_recipe_no_reviews(1, 5)

    assert get_recipe(1) == {'recipe_id': 1, 'user_id': user_id, 'ratings': 0, 'prep_time': 12, 'no_reviews': 5, 'method': 'This is a method', 'image': 'thisisimage', 'title': 'Recipe Title'}
'''

def get_recipe(recipe_id):
	'''Gets the information of the recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM recipes WHERE recipe_id = '{recipe_id}'")
	recipe = cur.fetchone()
	headers = [i[0] for i in cur.description]
	
	ret = {}
	if recipe is None:
		return None

	# Putting in dictionary
	for i in range(0, len(headers)):
		ret[headers[i]] = recipe[i]

	conn.commit()
	cur.close()
	conn.close()
	return ret

def get_ingredients_all():

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM ingredients")
    ingredients = cur.fetchall()
    return ingredients

def get_recipe_ingredients_all():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM recipe_ingredients")
    ingredients = cur.fetchall()
    return ingredients

'''
Tests for function to search recipes by name
'''

def test_search_recipe_name():
    reset_users()
    reset_recipes()
    add_user('zainridzuan', 'Zain', 'Ridzuan')
    add_recipe_db(1, 15, '1. Put water in the kettle and turn it on', '', 'Boiled water')
    recipe = search_recipe_name('Boiled water')
    print(recipe)
    assert recipe == {'recipes': [{'title': 'Boiled water', 'recipe_id': 1, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'no_reviews': 0, 'type': 'Other', "ingredients": []}]}

def test_search_multiple_recipe_names():
    reset_users()
    reset_recipes()
    add_user('zainridzuan', 'Zain', 'Ridzuan')
    add_recipe_db(1, 15, '1. Put water in the kettle and turn it on', '', 'Boiled water')
    add_recipe_db(1, 15, '1. Put water in the kettle and turn it on', '', 'Boiled water')
    recipe = search_recipe_name('Boiled water')
    assert recipe == {'recipes': [{'title': 'Boiled water', 'recipe_id': 1, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'no_reviews': 0, 'type': 'Other',   "ingredients": []}, {'title': 'Boiled water', 'recipe_id': 2, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'type': 'Other', 'no_reviews': 0,  "ingredients": []}]}

def test_search_partial_recipe_names():
    reset_users()
    reset_recipes()
    add_user('zainridzuan', 'Zain', 'Ridzuan')
    add_recipe_db(1, 15, '1. Put water in the kettle and turn it on', '', 'Boiled water')
    recipe = search_recipe_name('Boiled')
    assert recipe == {'recipes': [{'title': 'Boiled water', 'recipe_id': 1, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'no_reviews': 0, 'type': 'Other',  "ingredients": []}]}


def test_search_multiple_partial_recipe_names():
    reset_users()
    reset_recipes()
    add_user('zainridzuan', 'Zain', 'Ridzuan')
    add_recipe_db(1, 15, '1. Put water in the kettle and turn it on', '', 'Boiled water')
    add_recipe_db(1, 15, '1. Put ice in the kettle and turn it on', '', 'Boiled ice')
    recipe = search_recipe_name('Boi')
    print(recipe)
    assert recipe == {'recipes': [{'title': 'Boiled water', 'recipe_id': 1, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'no_reviews': 0, 'type': 'Other', "ingredients": []}, {'title': 'Boiled ice', 'type': 'Other', 'recipe_id': 2, 'user_id': 1, 'image': '', 'ratings': 0, 'prep_time': 15, 'no_reviews': 0,  "ingredients": []}]}

def test_search_non_existant_recipe():
    reset_users()
    reset_recipes()
    recipe = search_recipe_name('Boiled water')
    assert recipe == {'recipes': []}

def test_suggest_next_ingredients():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    list_of_ingredients = ['beef','chicken']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, [])
    assert next_ingredient == 'pork'

def test_suggest_next_ingredients1():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    list_of_ingredients = ['beef','chicken']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, [])
    assert next_ingredient == 'pork'

def test_suggest_next_ingredients2():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'pork'])
    list_of_ingredients = ['beef']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, [])
    assert next_ingredient == 'pork'

def test_suggest_next_ingredients3():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'pork'])
    list_of_ingredients = ['beef']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, ['pork'])
    assert next_ingredient is None

def test_suggest_next_ingredients4():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'pork'])
    list_of_ingredients = ['beef']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, ['chicken'])
    assert next_ingredient == 'pork'

def test_suggest_next_ingredients5():
    setup_server()
    user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id')
    add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken'], 'Dinner')
    add_recipe('id', 'Meatier sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    add_recipe('id', 'Meatiest sauce', 12, 'Meat', 'thisisimage', ['beef', 'pork'])
    list_of_ingredients = ['beef']
    next_ingredient = suggest_next_ingredient(list_of_ingredients, [], ['Dinner'])
    assert next_ingredient == 'chicken'

def test_add_reviews():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    assert get_review_from_recipe_id(recipe_id) == [{'review_id': review_id, 'user_id': 'id', 'recipe_id': recipe_id, 'rating': 2, 'comment': 'Commenting', 'username': 'szhou'}]

def test_adding_reviews_error():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    assert add_recipe_review('id', recipe_id, "Commenting", 2)['success'] == False
    assert json.loads(get_recipe_by_id(recipe_id)) == ({"recipe": {"recipe_id": 1, "user_id": 1, "ratings": 2.0, "prep_time": 12, "no_reviews": 1, "method": "Meat", "image": "thisisimage",
                                        "title": "Meat sauce", "username": "szhou", 'type': 'Other', "reviews": [{"review_id": 1, "user_id": 'id', "recipe_id": 1, "rating": 2, 'username': 'szhou', "comment": "Commenting"}],
                                        "ingredients": ["beef", "chicken", "pork"]}})

def test_adding_multiple_reviews():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    user_id2 = json.loads(user_registration('sum', "szhou", "szhou", 'ds@gmil.com', 'id1'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    review_id1 = add_recipe_review('id1', recipe_id, "Commenting2", 5)["review_id"]
    assert json.loads(get_recipe_by_id(recipe_id)) == ({"recipe": {"recipe_id": 1, 'type': 'Other', "user_id": 1, "ratings": 3.5, "prep_time": 12, "no_reviews": 2, "method": "Meat", "image": "thisisimage",
                                        "title": "Meat sauce", "username": "szhou", "reviews": [{"review_id": review_id, "user_id": 'id', "recipe_id": recipe_id, "rating": 2, "comment": "Commenting", 'username': 'szhou'},
                                        {"review_id": review_id1, "user_id": 'id1', "recipe_id": recipe_id, "rating": 5, "comment": "Commenting2", 'username': 'sum'}],
                                        "ingredients": ["beef", "chicken", "pork"]}})

def test_removing_reviews():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    user_id2 = json.loads(user_registration('sum', "szhou", "szhou", 'ds@gmil.com', 'id1'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    review_id1 = add_recipe_review('id1', recipe_id, "Commenting2", 5)["review_id"]
    assert json.loads(get_recipe_by_id(recipe_id)) == ({"recipe": {"recipe_id": 1, 'type': 'Other', "user_id": 1, "ratings": 3.5, "prep_time": 12, "no_reviews": 2, "method": "Meat", "image": "thisisimage",
                                        "title": "Meat sauce", "username": "szhou", "reviews": [{"review_id": review_id, "user_id": 'id', "recipe_id": recipe_id, "rating": 2, "comment": "Commenting", 'username': 'szhou'},
                                        {"review_id": review_id1, "user_id": 'id1', "recipe_id": recipe_id, "rating": 5, "comment": "Commenting2", 'username': 'sum'}],
                                        "ingredients": ["beef", "chicken", "pork"]}})
    assert delete_recipe_review('id', review_id1)['success'] == True
    print(json.loads(get_recipe_by_id(recipe_id)))
    assert json.loads(get_recipe_by_id(recipe_id)) == ({"recipe": {"recipe_id": 1, 'type': 'Other', "user_id": 1, "ratings": 2.0, "prep_time": 12, "no_reviews": 1, "method": "Meat", "image": "thisisimage",
                                        "title": "Meat sauce", "username": "szhou", "reviews": [{"review_id": 1, "user_id": 'id', "recipe_id": 1, "rating": 2, "comment": "Commenting", 'username': 'szhou'}],
                                        "ingredients": ["beef", "chicken", "pork"]}})

def test_edit_reviews():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    edit_recipe_review('id', review_id, "recomment", 1)
    assert get_review_from_recipe_id(recipe_id) == [{'review_id': review_id, 'user_id': 'id', 'recipe_id': recipe_id, 'rating': 1, 'comment': 'recomment', 'username': 'szhou'}]

def test_edit_reviews_error():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    user_id1 = json.loads(user_registration('szhoux', "szhou", "szhou", 'szhou@gmil.com', 'id1'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    assert edit_recipe_review('id1', review_id, "recomment", 1)['success'] == False

def test_delete_reviews_admin():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    user_id1 = json.loads(user_registration('szhoux', "szhou", "szhou", 'szhou@gmil.com', 'id1'))['user_id']
    recipe = add_recipe('id1', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_id = json.loads(recipe)['recipe_id']
    review_id = add_recipe_review('id', recipe_id, "Commenting", 2)["review_id"]
    assert delete_recipe_review('id', review_id)['success'] == True
    assert json.loads(get_recipe_by_id(recipe_id)) == ({"recipe": {"recipe_id": 1, 'type': 'Other', "user_id": user_id1, "ratings": 0, "prep_time": 12, "no_reviews": 0, "method": "Meat", "image": "thisisimage",
                                        "title": "Meat sauce", "username": "szhoux", "reviews": [],
                                        "ingredients": ["beef", "chicken", "pork"]}})
def test_sort_recipe_rating():
    setup_server()
    user_id_0 = json.loads(user_registration('test', "test", "test", 'test@gmil.com', 'id'))['user_id']
    user_id_1 = json.loads(user_registration('test1', "test1", "test1", 'test1@gmil.com', 'id1'))['user_id']
    recipe_0 = add_recipe('id1', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_1 = add_recipe('id1', 'Meat sauce v2', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'sauce'])
  
    
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    add_recipe_review('id', recipe_id_1["recipe_id"], "Comment", 5)
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']

    assert sort_recipes_rating([recipe_id_0, recipe_id_1]) == [recipe_id_1, recipe_id_0]


def test_sort_recipe_rating_more():
    setup_server()
    user_id_0 = json.loads(user_registration('test', "test", "test", 'test@gmil.com', 'id0'))['user_id']
    user_id_1 = json.loads(user_registration('test1', "test1", "test1", 'test1@gmil.com', 'id1'))['user_id']
    user_id_2 = json.loads(user_registration('test2', "test2", "test2", 'test2@gmil.com', 'id2'))['user_id']

    recipe_0 = add_recipe('id0', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_1 = add_recipe('id0', 'Meat sauce v2', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'sauce'])
    recipe_2 = add_recipe('id0', 'Meat sauce v3', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'lamb', 'sauce'])
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    recipe_id_2 = json.loads(get_recipe_by_id(3))['recipe']

    add_recipe_review('id1', recipe_id_1["recipe_id"], "Comment", 5)
    add_recipe_review('id2', recipe_id_1["recipe_id"], "Comment", 4)
    add_recipe_review('id2', recipe_id_2["recipe_id"], "Comment", 5)

    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    recipe_id_2 = json.loads(get_recipe_by_id(3))['recipe']
    
    assert sort_recipes_rating([recipe_id_0, recipe_id_1, recipe_id_2]) == [recipe_id_1, recipe_id_2, recipe_id_0]

def test_sort_recipe_no_reviews():
    setup_server()
    user_id_0 = json.loads(user_registration('test', "test", "test", 'test@gmil.com', 'id'))['user_id']
    user_id_1 = json.loads(user_registration('test1', "test1", "test1", 'test1@gmil.com', 'id1'))['user_id']
    recipe_0 = add_recipe('id1', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_1 = add_recipe('id1', 'Meat sauce v2', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'sauce'])
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    add_recipe_review('id', recipe_id_1["recipe_id"], "Comment", 5)
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']

    assert sort_recipes_no_reviews([recipe_id_0, recipe_id_1]) == [recipe_id_1, recipe_id_0]

def test_sort_recipe_no_reviews_more():
    setup_server()
    user_id_0 = json.loads(user_registration('test', "test", "test", 'test@gmil.com', 'id0'))['user_id']
    user_id_1 = json.loads(user_registration('test1', "test1", "test1", 'test1@gmil.com', 'id1'))['user_id']
    user_id_2 = json.loads(user_registration('test2', "test2", "test2", 'test2@gmil.com', 'id2'))['user_id']

    recipe_0 = add_recipe('id0', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe_1 = add_recipe('id0', 'Meat sauce v2', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'sauce'])
    recipe_2 = add_recipe('id0', 'Meat sauce v3', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork', 'lamb', 'sauce'])
    
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    recipe_id_2 = json.loads(get_recipe_by_id(3))['recipe']

    add_recipe_review('id1', recipe_id_1["recipe_id"], "Comment", 5)
    add_recipe_review('id1', recipe_id_2["recipe_id"], "Comment", 4)
    add_recipe_review('id2', recipe_id_2["recipe_id"], "Comment", 5)
    
    recipe_id_0 = json.loads(get_recipe_by_id(1))['recipe']
    recipe_id_1 = json.loads(get_recipe_by_id(2))['recipe']
    recipe_id_2 = json.loads(get_recipe_by_id(3))['recipe']
    
    assert sort_recipes_no_reviews([recipe_id_0, recipe_id_1, recipe_id_2]) == [recipe_id_2, recipe_id_1, recipe_id_0]

def test_get_recipes_by_type():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe1 = add_recipe('id', 'Meatier sauce', 1, 'Meathod', 'thisisimage', [], 'Breakfast')
    recipe2 = add_recipe('id', 'Meatiest sauce', 15, 'Meathod1', 'thisisimage', [], 'Dinner')
    recipe3 = add_recipe('id', 'Meatierest sauce', 2, 'Meathod2', 'thisisimage', [], 'Lunch')
    recipes = json.loads(get_recipe_all())['recipes']
    recipe_id = json.loads(recipe1)['recipe_id']
    
    assert get_recipes_by_type(recipes, ['Breakfast']) == [{'recipe_id': recipe_id, 'user_id': user_id, 'ratings': 0, 'prep_time': 1,
                                                            'no_reviews': 0, 'method': 'Meathod', 'image': 'thisisimage',
                                                            'title': 'Meatier sauce', 'type': 'Breakfast', 'reviews': [], 
                                                            'ingredients': [], 'username': 'szhou'}]

def test_get_many_recipes_by_type():
    setup_server()
    user_id = json.loads(user_registration('szhou', "szhou", "szhou", 'szhou@gmil.com', 'id'))['user_id']
    recipe = add_recipe('id', 'Meat sauce', 12, 'Meat', 'thisisimage', ['beef', 'chicken', 'pork'])
    recipe1 = add_recipe('id', 'Meatier sauce', 1, 'Meathod', 'thisisimage', [], 'Dinner')
    recipe2 = add_recipe('id', 'Meatiest sauce', 15, 'Meathod1', 'thisisimage', [], 'Dinner')
    recipe3 = add_recipe('id', 'Meatierest sauce', 2, 'Meathod2', 'thisisimage', [], 'Lunch')
    recipes = json.loads(get_recipe_all())['recipes']
    recipe_id1 = json.loads(recipe1)['recipe_id']
    recipe_id2 = json.loads(recipe2)['recipe_id']
    recipe_id = json.loads(recipe)['recipe_id']
    recipe_id3 = json.loads(recipe3)['recipe_id']

    assert get_recipes_by_type(recipes, ['Dinner']) == [{'recipe_id': recipe_id1, 'user_id': user_id, 'ratings': 0, 'prep_time': 1,
                                                            'no_reviews': 0, 'method': 'Meathod', 'image': 'thisisimage',
                                                            'title': 'Meatier sauce', 'type': 'Dinner', 'reviews': [], 
                                                            'ingredients': [], 'username': 'szhou'},
                                                            {'recipe_id': recipe_id2, 'user_id': user_id, 'ratings': 0, 'prep_time': 15,
                                                            'no_reviews': 0, 'method': 'Meathod1', 'image': 'thisisimage',
                                                            'title': 'Meatiest sauce', 'type': 'Dinner', 'reviews': [], 
                                                            'ingredients': [], 'username': 'szhou'}]
    
    assert get_recipes_by_type(recipes, ['Other']) == [{'recipe_id': recipe_id, 'user_id': user_id, 'ratings': 0, 'prep_time': 12,
                                                            'no_reviews': 0, 'method': 'Meat', 'image': 'thisisimage',
                                                            'title': 'Meat sauce', 'type': 'Other', 'reviews': [], 
                                                            'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'}]

    assert get_recipes_by_type(recipes, ['Lunch']) == [{'recipe_id': recipe_id3, 'user_id': user_id, 'ratings': 0, 'prep_time': 2,
                                                            'no_reviews': 0, 'method': 'Meathod2', 'image': 'thisisimage',
                                                            'title': 'Meatierest sauce', 'type': 'Lunch', 'reviews': [], 
                                                            'ingredients': [], 'username': 'szhou'}]

    assert get_recipes_by_type(recipes, ['Breakfast']) == []

    assert get_recipes_by_type(recipes,['Other', 'Lunch']) == [{'recipe_id': recipe_id, 'user_id': user_id, 'ratings': 0, 'prep_time': 12,
                                                            'no_reviews': 0, 'method': 'Meat', 'image': 'thisisimage',
                                                            'title': 'Meat sauce', 'type': 'Other', 'reviews': [], 
                                                            'ingredients': ['beef', 'chicken', 'pork'], 'username': 'szhou'},
                                                            {'recipe_id': recipe_id3, 'user_id': user_id, 'ratings': 0, 'prep_time': 2,
                                                            'no_reviews': 0, 'method': 'Meathod2', 'image': 'thisisimage',
                                                            'title': 'Meatierest sauce', 'type': 'Lunch', 'reviews': [], 
                                                            'ingredients': [], 'username': 'szhou'}]

    assert get_recipes_by_type(recipes, []) == recipes

