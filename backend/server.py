'''
The flask web server. Contains all accessible routes, and
calls functions that implement those routes, after doing some
basic setup (extraction of information from json/query string, etc.)
'''

import sys
from json import dumps
from flask import Flask, request, send_file
from flask_cors import CORS
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from recipe import *

from database import *
from admin import *
from user import user_registration, user_update, user_dashboard, list_all_users
from recipe import edit_recipe_review, delete_recipe_review, add_recipe, delete_recipe, update_recipe, get_recipe_by_id, get_recipe_by_user, get_recipe_all, get_ingredients, blacklist_ingredients, whitelist_ingredients, add_recipe_review, frequent_ingredients_without_recipe, get_recipes_by_type
from connection import get_conn_server_setup

has_started = False

def default_handler(err):
    '''
    Handles errors which occur throughout the server's lifespan
    '''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

def setup_server():
    conn = get_conn_server_setup()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT pg_terminate_backend(pg_stat_activity.pid)      \
        FROM pg_stat_activity                                           \
        WHERE pg_stat_activity.datname = 'fantastic_data';")
    cur.execute('drop database if exists fantastic_data')
    cur.execute('create database fantastic_data')
    conn.commit()
    cur.close()
    conn.close()

    launch_tables()


@APP.route("/")
def handle_landing_page():

    return 'Landing Page'

@APP.route("/api/users", methods=['POST'])
def handle_user_registration():

    data = request.get_json(force=True)
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    firebase_id = data['firebase_id']
    return user_registration(username, first_name, last_name, email, firebase_id= firebase_id)

@APP.route("/api/users/list/<user_id>", methods=['GET'])
def handle_user_list_all(user_id):

    return list_all_users(user_id)

@APP.route("/api/users/<firebase_id>", methods=['GET'])
def handle_user_dashboard(firebase_id):
    return user_dashboard(firebase_id)

@APP.route("/api/users/<user_id>", methods=['PUT'])
def handle_user_update(user_id):
    data = request.get_json(force=True)
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    return user_update(user_id, username, first_name, last_name)

@APP.route("/api/users/ban/<ban_user_id>", methods=['PUT'])
def ban_user_http(ban_user_id):
    header = request.headers['Authorization']
    return dumps(admin_ban_user(header.split("Bearer ")[1], ban_user_id))

@APP.route("/api/users/unban/<unban_user_id>", methods=['PUT'])
def unban_user_http(unban_user_id):
    header = request.headers['Authorization']
    return dumps(admin_unban_user(header.split("Bearer ")[1], unban_user_id))


@APP.route("/api/recipes", methods=['POST'])
def handle_add_recipe():

    data = request.get_json()
    firebase_id = data['firebase_id']
    title = data['title']
    prep_time = data['prep_time']
    method = data['method']
    image_url = data['image_url']
    ingredients = data['ingredients']
    mealType = data['type']
    return add_recipe(firebase_id, title, prep_time, method, image_url, ingredients, mealType)

@APP.route("/api/recipes", methods=["GET"])
def handle_search_recipe():
    args = request.args
    request.args.to_dict(flat=False)
    recipe_name = args.get("name")
    blacklisted_ingredients = args.getlist("blacklist")
    whitelisted_ingredients = args.getlist("whitelist")
    sort = args.get("sort")

    types = args.getlist("types")
    recipes = search_recipe_name(recipe_name)
    recipes = blacklist_ingredients(recipes["recipes"], blacklisted_ingredients)
    recipes = whitelist_ingredients(recipes, whitelisted_ingredients)
    recipes = get_recipes_by_type(recipes, types)

    if(sort == "ratings"):
        recipes = sort_recipes_rating(recipes)
    elif(sort == "reviews"):
        recipes = sort_recipes_no_reviews(recipes)

    return dumps(recipes)


@APP.route("/api/recipes/<recipe_id>", methods=['DELETE'])
def handle_delete_recipe(recipe_id):

    data = request.get_json()
    requesting_user_id = data['requesting_user_id']
    return delete_recipe(recipe_id, requesting_user_id)

@APP.route("/api/recipes/<recipe_id>", methods=['PUT'])
def handle_update_recipe(recipe_id):

    data = request.get_json()
    firebase_id = data['firebase_id']
    title = data['title']
    prep_time = data['prep_time']
    method = data['method']
    image_url = data['image_url']
    return update_recipe(firebase_id, recipe_id, title, prep_time, method, image_url)

@APP.route("/api/recipes/<recipe_id>", methods=['GET'])
def handle_get_recipe_by_id(recipe_id):
    return get_recipe_by_id(recipe_id)

@APP.route("/api/recipes/user/<user_id>", methods=['GET'])
def handle_get_recipe_by_user(user_id):
    return get_recipe_by_user(user_id)

@APP.route("/api/recipes", methods=['GET'])
def handle_get_recipe_all():
    return get_recipe_all()

@APP.route("/api/ingredients", methods=['GET'])
def handle_get_ingredients():
    return get_ingredients()

@APP.route("/api/ingredients/blacklist", methods=['GET'])
def handle_blacklist_ingredients():

    args = request.args
    recipes = args.get("recipes")
    ingredients = args.get("blacklist")
    return blacklist_ingredients(recipes, ingredients)

@APP.route("/api/ingredients/whitelist", methods=['GET'])
def handle_whitelist_ingredients():

    args = request.args
    recipes = args.get("recipes")
    ingredients = args.get("whitelist")
    return whitelist_ingredients(recipes, ingredients)

@APP.route("/api/ingredients/suggest", methods=['GET'])
def handle_suggest_next_ingredient():
    args = request.args
    whitelist_ingredients = args.getlist("whitelist")
    blacklist_ingredients = args.getlist("blacklist")
    types = args.getlist("types")

    return dumps({'ingredient': suggest_next_ingredient(whitelist_ingredients, blacklist_ingredients, types)})

@APP.route("/api/ingredients/frequent_ingredients", methods=['GET'])
def handle_frequent_ingredients():
    return frequent_ingredients_without_recipe()

@APP.route("/api/recipes/review", methods=['POST'])
def handle_add_recipe_review():
    data = request.get_json()
    recipe_id = data["recipe_id"]
    comment = data["comment"]
    rating = data["rating"]
    firebase_id = data["firebase_id"]
    return dumps(add_recipe_review(firebase_id, recipe_id, comment, rating))

@APP.route("/api/recipes/review", methods=['PUT'])
def handle_edit_recipe_review():
    data = request.get_json()
    comment = data["comment"]
    rating = data["rating"]
    firebase_id = data["firebase_id"]
    review_id = data["review_id"]
    return dumps(edit_recipe_review(firebase_id, review_id, comment, rating))

@APP.route("/api/recipes/review", methods=['DELETE'])
def handle_delete_recipe_review():
    data = request.get_json()
    firebase_id = data["firebase_id"]
    review_id = data["review_id"]
    return dumps(delete_recipe_review(firebase_id, review_id))


if __name__ == "__main__":
    setup_server()
    launch_tables()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
