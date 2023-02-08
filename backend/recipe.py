'''
Implementation of Recipe related functions
'''

from pickle import TRUE
from webbrowser import get
import psycopg2
from error import InputError
from json import dumps, loads
from connection import get_conn
from database import edit_recipe_no_reviews, edit_recipe_rating, get_review_from_review_id, delete_review, get_recipe, get_user_dict, get_user_dict_by_firebase, get_ingredient_id, get_ingredient, get_review_from_recipe_id, add_review, edit_comment, edit_rating


def add_recipe(firebase_id, title, prep_time, method, image_url, ingredients, type = 'Other'):
    user_id = get_user_dict_by_firebase(firebase_id)['user_id']

    conn = get_conn()
    cur = conn.cursor()


    cur.execute("INSERT INTO recipes (user_id, prep_time, no_reviews, method, image, title, ratings, type)  \
			    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)                                              \
				RETURNING recipe_id",
                (int(user_id), int(prep_time), '0', method, image_url, title, '0', type))
    recipe_id = cur.fetchone()[0]
    conn.commit()

    ingredients = list(dict.fromkeys(ingredients))
    for ingredient in ingredients:
        cur.execute('''INSERT INTO ingredients(name)
                    SELECT (%s)
                    WHERE not exists (SELECT 1 from ingredients where name=%s)''',
                    (ingredient, ingredient))
    conn.commit()

    for ingredient in ingredients:
        cur.execute('''select ingredient_id from ingredients where name=%s''',
                    (ingredient,))
        ingredient_id = cur.fetchone()[0]
        cur.execute('''INSERT INTO recipe_ingredients(ingredient_id, recipe_id)
                       SELECT %s, %s
                       WHERE not exists (SELECT 1 from recipe_ingredients where (ingredient_id=%s and recipe_id=%s))''',
                       (ingredient_id, recipe_id, ingredient_id, recipe_id))

    conn.commit()
    cur.close()
    conn.close()

    return dumps({
        'recipe_id' : recipe_id,
    })

def add_recipe_review(firebase_id, recipe_id, comment, rating):
    if rating is None: return {'success': False}

    user_id = get_user_dict_by_firebase(firebase_id)["user_id"]

    for x in get_review_from_recipe_id(recipe_id):
        if firebase_id == x['user_id']:
            return {'success': False}

    review_id = add_review(user_id, recipe_id, comment, rating)
    recipe = loads(get_recipe_by_id(recipe_id))['recipe']
    recipe_rating = recipe['ratings']
    recipe_no_reviews = recipe['no_reviews']
    recipe_new_rating = ((recipe_rating * recipe_no_reviews) + int(rating)) / (recipe_no_reviews + 1)

    edit_recipe_no_reviews(recipe_id, recipe_no_reviews + 1)
    edit_recipe_rating(recipe_id, recipe_new_rating)
    return {'success': True, 'review_id': review_id}

def edit_recipe_review(firebase_id, review_id, comment, rating):
    user_id = get_user_dict_by_firebase(firebase_id)['user_id']

    review = get_review_from_review_id(review_id)[0]

    if user_id != review['user_id']:
        return {'success': False}

    edit_comment(review_id, comment)

    recipe = get_recipe(review['recipe_id'])
    old_rating = review["rating"]
    recipe_rating = recipe['ratings']
    recipe_no_reviews = recipe['no_reviews']
    recipe_new_rating = ((recipe_rating * recipe_no_reviews) + rating - old_rating) / (recipe_no_reviews)

    edit_recipe_rating(review['recipe_id'], recipe_new_rating)
    edit_rating(review_id, rating)

    return {'success': True}

def delete_recipe_review(firebase_id, review_id):
    user = get_user_dict_by_firebase(firebase_id)
    review = get_review_from_review_id(review_id)[0]

    if user['user_id'] != review['user_id'] and user['is_admin'] is False:
        return {'success': False}

    recipe = get_recipe(review['recipe_id'])
    rating = review["rating"]
    recipe_rating = recipe['ratings']
    recipe_no_reviews = recipe['no_reviews']
    if recipe_no_reviews > 1:
        recipe_new_rating = ((recipe_rating * recipe_no_reviews) - rating) / (recipe_no_reviews - 1)
    else:
        recipe_new_rating = 0

    delete_review(review_id)
    edit_recipe_rating(recipe['recipe_id'], recipe_new_rating)
    edit_recipe_no_reviews(recipe['recipe_id'], recipe_no_reviews - 1)
    return {'success': True}

def delete_recipe(recipe_id, requesting_user_id):

    recipe = get_recipe(recipe_id)
    user = get_user_dict_by_firebase(requesting_user_id)

    # checking that the user is either the admin, or the creator of the recipe
    if (get_user_dict(recipe['user_id'])['firebase_id'] == requesting_user_id or user['is_admin'] == True):
        conn = get_conn()

        cur = conn.cursor()
        cur.execute("DELETE FROM recipes WHERE recipe_id=%s", (recipe_id,))

        conn.commit()
        cur.close()
        conn.close()

        # Deleting affiliated reviews
        reviews = get_review_from_recipe_id(recipe_id)

        for i in reviews:
            delete_review(i['review_id'])

        return dumps({
            'success' : True,
        })
    else:
        return dumps({
            'success' : False,
        })

def update_recipe(firebase_id, recipe_id, title, prep_time, method, image_url):
    user_id = get_user_dict_by_firebase(firebase_id)['user_id']

    recipe = get_recipe(recipe_id)
    if not recipe['user_id'] == user_id:
        return dumps({
            'success': False,
        })

    conn = get_conn()

    cur = conn.cursor()
    cur.execute("UPDATE recipes SET title=%s WHERE recipe_id=%s", (title, recipe_id))
    cur.execute("UPDATE recipes SET prep_time=%s WHERE recipe_id=%s", (prep_time, recipe_id))
    cur.execute("UPDATE recipes SET method=%s WHERE recipe_id=%s", (method, recipe_id))
    cur.execute("UPDATE recipes SET image=%s WHERE recipe_id=%s", (image_url, recipe_id))

    conn.commit()
    cur.close()
    conn.close()
    return dumps({
            'success': True,
        })


def get_recipe_by_id(recipe_id):

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM recipes WHERE recipe_id = '{recipe_id}'")
    recipe = cur.fetchone()
    headers = [i[0] for i in cur.description]

    ret = {}
    if recipe is None: return None

    for i in range(0, len(headers)):
        ret[headers[i]] = recipe[i]

    ret['username'] = get_user_dict(ret['user_id'])['username']

    reviews = get_review_from_recipe_id(recipe_id)
    ret['reviews'] = reviews

    ingredients = []
    cur.execute(f"SELECT ingredient_id FROM recipe_ingredients WHERE recipe_id = '{recipe_id}'")
    ingredient_ids = cur.fetchall()
    for iid in ingredient_ids:
        iid = iid[0]
        cur.execute(f"SELECT name FROM ingredients WHERE ingredient_id = '{iid}'")
        ingredients.append(cur.fetchone()[0])

    ret['ingredients'] = ingredients

    conn.commit()
    cur.close()
    conn.close()

    return dumps({
        'recipe': ret
    })

def get_recipe_by_user(firebase_id):

    conn = get_conn()
    cur = conn.cursor()
    id = get_user_dict_by_firebase(firebase_id)['user_id']
    cur.execute(f"SELECT recipe_id FROM recipes WHERE user_id = '{id}'")
    recipe_ids = cur.fetchall()
    sorted(recipe_ids)
    recipes = []
    for recipe_id in recipe_ids:

        recipe_id = recipe_id[0]
        recipe = loads(get_recipe_by_id(recipe_id))['recipe']
        recipes.append(recipe)


    return dumps({
        'recipes': recipes,
    })

def get_recipe_all():

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT recipe_id FROM recipes")
    recipe_ids = cur.fetchall()

    recipes = []
    for recipe_id in recipe_ids:

        recipe_id = recipe_id[0]
        recipe = loads(get_recipe_by_id(recipe_id))['recipe']
        recipes.append(recipe)


    return dumps({
        'recipes': recipes,
    })

def get_ingredients():

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM ingredients")
    ingredients_data = cur.fetchall()

    ingredients = []
    for data in ingredients_data:
        ingredients.append(data[0])

    return dumps({
        'ingredients': ingredients,
    })

def blacklist_ingredients(recipes, blacklisted_ingredients):

    result = []
    if(blacklisted_ingredients != None and len(blacklisted_ingredients) != 0 and ',' in blacklisted_ingredients[0]):
        blacklisted_ingredients[0] = blacklisted_ingredients[0].replace(" ", "")
        blacklisted_ingredients = blacklisted_ingredients[0].split(",")

    if(blacklisted_ingredients == None or blacklisted_ingredients == [] or len(blacklisted_ingredients[0]) == 0):
        return recipes

    for recipe in recipes:
        recipe_ingredient = recipe['ingredients']
        if not any(item in recipe_ingredient for item in blacklisted_ingredients):
            result.append(recipe)

    return result

def whitelist_ingredients(recipes, whitelisted_ingredients):


    result = []
    if(whitelisted_ingredients != None and len(whitelisted_ingredients) != 0 and ',' in whitelisted_ingredients[0]):
        whitelisted_ingredients[0] =  whitelisted_ingredients[0].replace(" ", "")
        whitelisted_ingredients = whitelisted_ingredients[0].split(",")

    if(whitelisted_ingredients == None or whitelisted_ingredients == [] or len(whitelisted_ingredients[0]) == 0):
        return recipes


    for recipe in recipes:
        recipe_ingredient = recipe['ingredients']
        if set(whitelisted_ingredients).issubset(set(recipe_ingredient)):
            result.append(recipe)

    return result

def search_recipe_name(recipe_name):
    conn = get_conn()
    cur = conn.cursor()

    # Searches the db for any recipe with matching name
    if recipe_name != None:
        recipe_name = recipe_name.lower()
        cur.execute(f"SELECT title, recipe_id, user_id, image, ratings, prep_time, no_reviews, type	\
                    FROM recipes                                                                    \
                    WHERE LOWER(title) LIKE '{recipe_name}%'")
    else:
        # If there is NoneType for recipe_name,
        # all recipes should be returned
        cur.execute(f"SELECT * FROM recipes")

    # Converts array into JSON array
    row_headers=[x[0] for x in cur.description]
    json_recipes = []
    recipes = cur.fetchall()


    for result in recipes:
        recipe = dict(zip(row_headers,result))
        recipe_id = recipe['recipe_id']

        cur.execute(f"SELECT ingredient_id FROM recipe_ingredients WHERE recipe_id = '{recipe_id}'")
        ingredients = []
        ingredient_ids = cur.fetchall()
        for iid in ingredient_ids:
            iid = iid[0]
            cur.execute(f"SELECT name FROM ingredients WHERE ingredient_id = '{iid}'")
            ingredients.append(cur.fetchone()[0])
        recipe["ingredients"] = ingredients
        json_recipes.append(recipe)

    cur.close()

    return {"recipes": json_recipes}

# ingredient_id_list = [0, 1, 2, 4, 5]
def suggest_next_ingredient(whitelist_ingredient, blacklist, types = []):
    conn = get_conn()
    cur = conn.cursor()
    recipes = loads(get_recipe_all())['recipes']

    whitelist_recipes = whitelist_ingredients(recipes, whitelist_ingredient)
    final_recipes = blacklist_ingredients(whitelist_recipes, blacklist)
    final_recipes = get_recipes_by_type(final_recipes, types)

    whitelist = ", ".join(str(get_ingredient_id(i)) for i in whitelist_ingredient)

    int_recipes = "', '".join(str(i['recipe_id']) for i in final_recipes)
    int_recipes = "'" + int_recipes + "'"

    if final_recipes == []:
        return None

    cur.execute(f"SELECT ingredient_id                                                             \
                  FROM recipe_ingredients                                                          \
                  WHERE ingredient_id NOT IN ({whitelist}) AND recipe_id IN ({int_recipes})        \
                  GROUP BY ingredient_id                                                            \
                  ORDER BY count(ingredient_id) DESC                                                \
                  ")
    results = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return get_ingredient(results)

# takes in a list of recipe id's and returns the recipe id's sorted by their rating
def sort_recipes_rating(recipes_list):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f"SELECT AVG(ratings)                                                             \
                  FROM recipes")

    avg_rating = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    # This formula gives the true Bayesian estimate which is the same that IMDb used to use
    m = 2
    sorted_dict = sorted(recipes_list, 
                key=lambda recipe: (recipe["ratings"] * recipe["no_reviews"] + avg_rating * m)/(recipe["no_reviews"] + m), reverse = True)

    return sorted_dict

# takes in a list of recipe id's and returns the recipe id's sorted by the number of reviews
def sort_recipes_no_reviews(recipes_list):
    sorted_dict = sorted(recipes_list, key=lambda recipe: recipe["no_reviews"], reverse = True)
    return sorted_dict

def frequent_ingredients_without_recipe():
    '''
    Most popular recipes taken from https://www.soupersage.com/blog/30-most-popular-recipe-ingredients-2019/
    '''

    frequent_ingredients_set = set(['olive oil', 'chicken', 'butter', 'egg', 'rice', 'pork', 'beef',
                                 'cheese', 'garlic', 'turkey', 'onion', 'corn', 'milk'])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''SELECT name
                FROM recipe_ingredients LEFT OUTER JOIN ingredients
                on recipe_ingredients.ingredient_id = ingredients.ingredient_id''')

    ingredients = results = cur.fetchall()
    available_ingredients_set = set()
    for ing in ingredients:
        available_ingredients_set.add(ing[0])

    ingredients_without_recipe = list(frequent_ingredients_set.difference(available_ingredients_set))
    return dumps({
        'ingredients_without_recipe' : ingredients_without_recipe,
    })

def get_recipes_by_type(recipes, types):
    ret = []
    if(types != None and len(types) != 0 and ',' in types[0]):
        types[0] = types[0].replace(" ", "")
        types = types[0].split(",")

    if(types == None  or types == [] or len(types[0]) == 0):
        return recipes

    for recipe in recipes:
        recipe_type = recipe['type']
        if recipe_type in types:
            ret.append(recipe)

    return ret
