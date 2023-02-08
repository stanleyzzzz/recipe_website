from webbrowser import get
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from connection import get_conn

def launch_tables():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'CREATE TABLE IF NOT EXISTS public.users                                   \
			(                                                                               \
			user_id serial,        															\
			is_admin boolean,                                                               \
			first_name text COLLATE pg_catalog."default",                                   \
			last_name text COLLATE pg_catalog."default",                                    \
			username text COLLATE pg_catalog."default",                                     \
			email text COLLATE pg_catalog."default",                                        \
			is_banned boolean,                                                              \
			firebase_id text,																\
			CONSTRAINT users_pkey PRIMARY KEY (user_id),                                    \
			CONSTRAINT "unique" UNIQUE (username, firebase_id)								\
			)')	

	cur.execute('CREATE TABLE IF NOT EXISTS public.recipes                                  \
			(                                                                               \
			recipe_id serial,  \
			user_id integer NOT NULL,                                                       \
			ratings real,                                                                   \
			prep_time integer,                                                              \
			no_reviews integer,                                                             \
			method text COLLATE pg_catalog."default",                                       \
			image text COLLATE pg_catalog."default",                                        \
			type text,																		\
			title text COLLATE pg_catalog."default",                                        \
			CONSTRAINT recipes_pkey PRIMARY KEY (recipe_id)                                 \
			)')

	cur.execute('CREATE TABLE IF NOT EXISTS public.reviews                                  \
			(                                                                               \
			review_id serial,																\
			user_id integer,                                                                \
			recipe_id integer REFERENCES recipes ON DELETE CASCADE,                         \
			rating integer,                                                                 \
			comment text COLLATE pg_catalog."default",                                      \
			CONSTRAINT reviews_pkey PRIMARY KEY (review_id)                                 \
			)')

	
	cur.execute('CREATE TABLE IF NOT EXISTS public.ingredients                                              \
			(                                                                                               \
			ingredient_id serial,      																		\
			name text COLLATE pg_catalog."default",                                                         \
			CONSTRAINT ingredients_pkey PRIMARY KEY (ingredient_id)                                         \
			)')

	cur.execute('CREATE TABLE IF NOT EXISTS public.recipe_ingredients                       \
			(                                                                               \
			ingredient_id integer REFERENCES ingredients ON DELETE CASCADE,  				\
			recipe_id integer REFERENCES recipes ON DELETE CASCADE,                         \
			amount text																		\
			)')

	


	conn.commit()
	cur.close()
	conn.close()

def reset_all_tables():
	reset_recipe_ingredients()
	reset_ingredients()
	
	reset_users()
	reset_recipes()


def reset_users():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'TRUNCATE users RESTART IDENTITY;')
	conn.commit()
	cur.close()
	conn.close()
	
def reset_recipes():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'TRUNCATE recipes RESTART IDENTITY CASCADE;')
	conn.commit()
	cur.close()
	conn.close()

def reset_ingredients():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'TRUNCATE ingredients RESTART IDENTITY CASCADE;')
	conn.commit()
	cur.close()
	conn.close()

def reset_reviews():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'TRUNCATE reviews RESTART IDENTITY;')
	conn.commit()
	cur.close()
	conn.close()

def reset_recipe_ingredients():
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f'TRUNCATE recipe_ingredients RESTART IDENTITY;')
	conn.commit()
	cur.close()
	conn.close()

'''USER TABLE FUNCTIONS'''

def add_user(username, first_name, last_name, is_admin = False, is_banned = False, email = None, firebase_id = None):
	'''Add the username'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"INSERT INTO users (firebase_id, username, first_name, last_name, is_admin, is_banned, email)\
			VALUES ('{firebase_id}', '{username}', '{first_name}', '{last_name}', '{is_admin}', '{is_banned}', '{email}')\
				RETURNING user_id")


	user_id = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return user_id

def delete_user(user_id):
	'''Delete user FOR TESTING'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")

	conn.commit()
	cur.close()
	conn.close()

def is_admin(user_id):
	'''Check if user_id is admin'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT is_admin FROM users WHERE firebase_id = '{user_id}'")
	ret = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return ret

def edit_username(user_id, username):
	'''Change the username of the user_id'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE users SET username = '{username}' WHERE user_id = '{user_id}'")

	conn.commit()
	cur.close()
	conn.close()

def ban_user(user_id):
	'''Ban the selected user_id'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE users SET is_banned = True WHERE user_id = '{user_id}'")

	conn.commit()
	cur.close()
	conn.close()

def unban_user(user_id):
	'''Unban the selected user_id'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE users SET is_banned = False WHERE user_id = '{user_id}'")

	conn.commit()
	cur.close()
	conn.close()
        
def get_user_dict(user_id):
	'''Get user's information'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
	user = cur.fetchone()
	
	if user is None:
		return None

	headers = [i[0] for i in cur.description]
	
	ret = {}

	# Putting in dictionary
	for i in range(0, len(headers)):
		ret[headers[i]] = user[i]
		
		if headers[i] == 'email' and user[i] == "None":
			ret[headers[i]] = None

	conn.commit()
	cur.close()
	conn.close()

	return ret

def get_user_dict_by_firebase(firebase_id):
	'''Get user's information'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM users WHERE firebase_id = '{firebase_id}'")
	user = cur.fetchone()
	
	if user is None:
		return None

	headers = [i[0] for i in cur.description]
	
	ret = {}

	# Putting in dictionary
	for i in range(0, len(headers)):
		ret[headers[i]] = user[i]
		
		if headers[i] == 'email' and user[i] == "None":
			ret[headers[i]] = None

	conn.commit()
	cur.close()
	conn.close()

	return ret

def get_user_id(username):
	'''Get the user id of the specified username'''
	conn = get_conn()
	
	cur = conn.cursor()
	cur.execute(f"SELECT user_id FROM users WHERE username = '{username}'")
	
	user_id = cur.fetchone()
	if user_id is None:
		return None
	conn.commit()
	cur.close()
	conn.close()

	return user_id[0]

'''RECIPE TABLE FUNCTIONS'''
def add_recipe_db(user_id, prep_time, method, image_url, title, type = "Other"):
	'''Adding a recipe'''
	conn = get_conn()
	cur = conn.cursor()
	cur.execute("INSERT INTO recipes (user_id, prep_time, no_reviews, method, image, title, ratings, type)  \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)                                              \
				RETURNING recipe_id",
				(int(user_id), int(prep_time), '0', method, image_url, title, '0', type))
	recipe_id = cur.fetchone()[0]
	conn.commit()
	cur.close()
	conn.close()
	return recipe_id


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

def remove_recipe(recipe_id):
	'''Remove a recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"DELETE FROM recipes WHERE recipe_id = {recipe_id}")

	conn.commit()	
	cur.close()
	conn.close()

def edit_recipe_method(recipe_id, method):
	'''Edit the method of the recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE recipes SET method = '{method}' WHERE recipe_id = {recipe_id}")

	conn.commit()	
	cur.close()
	conn.close()

def edit_recipe_rating(recipe_id, ratings):
	'''Edit the recipe rating'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE recipes SET ratings = {ratings} WHERE recipe_id = {recipe_id}")

	conn.commit()
	cur.close()
	conn.close()

def edit_recipe_no_reviews(recipe_id, no_reviews):
	'''Edit the number of recipe ratings'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE recipes SET no_reviews = {no_reviews} WHERE recipe_id = {recipe_id}")

	conn.commit()
	cur.close()
	conn.close()

'''REVIEW TABLE FUNCTIONS'''
def add_review(user_id, recipe_id, comment, rating):
	'''Adds a review'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"INSERT INTO reviews (user_id, recipe_id, comment, rating)\
			VALUES ('{user_id}', '{recipe_id}', '{comment}', '{rating}')\
				RETURNING review_id")


	review_id = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return review_id

def edit_comment(review_id, comment):
	'''Edit Comment'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE reviews SET comment = '{comment}'\
				WHERE review_id = {review_id}")

	conn.commit()
	cur.close()
	conn.close()

def delete_review(review_id: int):
	'''Delete review'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"DELETE FROM reviews\
				WHERE review_id = {review_id}")

	conn.commit()
	cur.close()
	conn.close()

def get_review_from_recipe_id(recipe_id):
	'''Get all review objects from a recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM reviews WHERE recipe_id = {recipe_id}")
	
	reviews = cur.fetchall()

	ret = []

	if reviews is None:
		return None
	
	headers = [i[0] for i in cur.description]
	# Putting in dictionary
	for x in reviews:
		review_dicts = {}
		user = None
		for i in range(0, len(headers)):
			if headers[i] != 'user_id':
				review_dicts[headers[i]] = x[i]
			else:
				user = get_user_dict(x[i])
				review_dicts[headers[i]] = user['firebase_id']
		review_dicts['username'] = user['username']
		ret.append(review_dicts)


	return ret

def get_review_from_review_id(review_id):
	'''Get all reviews from a recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM reviews WHERE review_id = {review_id}")
	
	reviews = cur.fetchall()

	ret = []

	if reviews is None:
		return None
	
	headers = [i[0] for i in cur.description]
	# Putting in dictionary
	for x in reviews:
		review_dicts = {}
		for i in range(0, len(headers)):
			review_dicts[headers[i]] = x[i]
		
		ret.append(review_dicts)

	return ret

def edit_rating(review_id: int, rating: int):
	'''Edit review's rating'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE reviews SET rating = '{rating}' WHERE review_id = {review_id}")
		
	conn.commit()
	cur.close()
	conn.close()


'''INGREDIENT TABLE FUNCTIONS'''
def add_ingredient(name):
	'''Add ingredient'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"INSERT INTO ingredients (name)\
			VALUES ('{name}')\
				RETURNING ingredient_id")


	ingredient_id = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return ingredient_id

def get_ingredient(id):
	'''Get the text for the ingredient'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT name FROM ingredients WHERE ingredient_id = {id}")

	ingredient_name = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return ingredient_name

def get_ingredient_id(name):
	'''Get the id for the ingredient'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT ingredient_id FROM ingredients WHERE name = '{name}'")

	ingredient_id = cur.fetchone()[0]

	conn.commit()
	cur.close()
	conn.close()

	return ingredient_id

'''RECIPE_INGREDIENTS TABLE FUNCTIONS'''
def add_recipe_ingredients(ingredient_id, recipe_id, amount= None):
	'''Add a connection for ingredients and recipes'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"INSERT INTO recipe_ingredients (ingredient_id, recipe_id, amount)\
		 VALUES ('{ingredient_id}', '{recipe_id}', '{amount}')")
	
	conn.commit()
	cur.close()
	conn.close()

def remove_recipe_ingredients(ingredient_id, recipe_id):
	'''Remove a connection for ingredients and recipes'''
	conn = get_conn()

	cur = conn.cursor()

	cur.execute(f"DELETE FROM recipe_ingredients WHERE ingredient_id = '{ingredient_id}' AND recipe_id = {recipe_id}")
	
	conn.commit()
	cur.close()
	conn.close()

def update_recipe_ingredients_amount(ingredient_id, recipe_id, amount):
	'''Update a connection for ingredients and recipes'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"UPDATE recipe_ingredients SET amount = {amount} WHERE ingredient_id = '{ingredient_id}' AND recipe_id = {recipe_id}")
	
	conn.commit()
	cur.close()
	conn.close()

def get_recipes_ingredients(recipe_id):
	'''Returns all the ingredients for the recipe'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM recipe_ingredients WHERE recipe_id = {recipe_id}")

	recipe_ing = cur.fetchall()

	ret = []

	if recipe_ing is None:
		return []
	
	headers = [i[0] for i in cur.description]
	# Putting in dictionary
	for x in recipe_ing:
		ing_dict = {}
		for i in range(0, len(headers)):
			ing_dict[headers[i]] = x[i]

		
		ret.append(ing_dict)

	return ret

def get_recipes_by_ingredients(ingredient_id):
	'''Returns all the recipes which includes the ingredient'''
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT * FROM recipe_ingredients WHERE ingredient_id = {ingredient_id}")

	recipe_ing = cur.fetchall()

	ret = []

	if recipe_ing is None:
		return None
	
	headers = [i[0] for i in cur.description]
	# Putting in dictionary
	for x in recipe_ing:
		recipe_dict = {}
		for i in range(0, len(headers)):
			recipe_dict[headers[i]] = x[i]
		
		ret.append(recipe_dict)
	
	return ret

def search_recipe_by_name(recipe_name):
	conn = get_conn()

	cur = conn.cursor()
	cur.execute(f"SELECT *					\
				  FROM recipes WHERE title={recipe_name}")
	ret = cur.fetchall()


	cur.close()
	conn.close()

	return ret

