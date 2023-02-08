# command can be run like this: ./insert_dummy_data.sh 8080 1

if [ $2 = 1 ]; then
# Create an admin user
curl -X POST http://127.0.0.1:$1/api/users -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
'{"username": "TestingAdmin", "first_name": "Adam", "last_name": "Min", "email": "testing@email.com", "firebase_id": "4wYXRpDETSXpkASca8dCOxV5rdh1" }'

curl -X POST http://127.0.0.1:$1/api/users -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
'{"username": "chetfakeaccount", "first_name": "Chet", "last_name": "Faker", "email": "fakeuser@email.com", "firebase_id": "gP7Rn7Cf7UYIr9D3Gol0BGVeFwl1" }'

curl -X POST http://127.0.0.1:$1/api/users -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
'{"username": "123", "first_name": "John", "last_name": "Doe", "email": "lingat917@email.com", "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2" }'



curl -X POST http://127.0.0.1:$1/api/users -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
'{"username": "JaneSmithing", "first_name": "Jane", "last_name": "Smith", "email": "zainridzuan@gmail.com", "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2" }'

curl -X POST http://127.0.0.1:$1/api/users -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
'{"username": "CraigPelton", "first_name": "Craig", "last_name": "Pelton", "email": "someone@email.com", "firebase_id": "jYskbOSiNCNaP1xdYohN9Hmn1n52" }'
# List single user 
curl -X GET http://127.0.0.1:$1/api/users/W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2

# List all users
curl -X GET http://127.0.0.1:$1/api/users/list/W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2

# Create a recipe 
curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "jYskbOSiNCNaP1xdYohN9Hmn1n52",
   "firebase_id": "jYskbOSiNCNaP1xdYohN9Hmn1n52",
    "title": "Adobo", 
    "prep_time": 120,
     "method": "1. Combine Chicken and Marinade ingredients in a bowl. Marinate for at least 20 minutes, or up to overnight.\n2. Heat 1 tbsp oil in a skillet over high heat. Remove chicken from marinade (reserve marinade) and place in the pan. Sear both sides until browned  about 1 minute on each side. Do not cook the chicken all the way through.\n3. Remove chicken skillet and set aside.\n4. Heat the remaining oil in skillet. Add garlic and onion, cook 1 1/2 minutes.\n5. Add the reserved marinade, water, sugar and black pepper. Bring it to a simmer then turn heat down to medium high. Simmer 5 minutes.\n6. Add chicken smooth side down. Simmer uncovered for 20 to 25 minutes (no need to stir), turning chicken at around 15 minutes, until the sauce reduces down to a thick jam-like syrup.", 
     "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Chicken_adobo.jpg/1200px-Chicken_adobo.jpg", 
     "ingredients": ["chicken", "garlic"],
     "type": "Dinner"  }'

curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
   "firebase_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
    "title": "Fried Rice", 
    "prep_time": 60, 
    "method": "1. Use cold rice: Yove gotta plan ahead and use thoroughly-chilled cooked rice. A fresh batch of warm (or even lukewarm) rice will not fry well when it hits the hot pan, and will result in soggy and sticky clumps — no good. So leftover refrigerated rice is ideal! Or, if you are in a hurry (or have an impulse craving for fried rice, which I completely understand ?), just cook up a fresh batch of rice. Then spread it out on a baking sheet or another large flat pan, drape the rice with a layer of plastic wrap, then pop it in the fridge for 30 minutes (or in the freezer for 10-15 minutes) until it is thoroughly chilled (not frozen).\n2. Use butter: Yes, butter. I have made many a batch of fried rice using various oils, and Im now convinced theres a reason why Japanese steak houses use that big slab of butter when theyre making fried rice. It just tastes so much better, and also makes everything brown up perfectly. (Although by contrast to Japanese steak houses, we only use 3 tablespoons for a large batch of rice in this recipe.)\n3. Use veggies: This is one of my big pet peeves with lame take-out fried rice — not enough veggies! In addition to adding some nice spots of color, veggies go a long way in adding some flavor and freshness to fried rice. Our local Chinese restaurant always added both white and green onions, too, which I included in this recipe. But feel free to modernize this recipe with some other delicious stir-fried veggies as well!", 
    "image_url": "https://www.seriouseats.com/thmb/quM8-Bh0abni-O0ikBpJn0KaH00=/1500x844/smart/filters:no_upscale()/easy-vegetable-fried-rice-recipe-hero-2-fed2a62b8bce4c51b945d9c24c2edb68.jpg", 
    "ingredients": ["onion", "rice"],
    "type": "Lunch"   }'


curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2",
   "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2",
    "title": "Pumpkin Soup", 
    "prep_time": 30, 
    "method": "1. something", 
    "image_url": "https://media.healthyfood.com/wp-content/uploads/2019/07/Creamy-pumpkin-soup.jpg", 
    "ingredients": ["pumpkin"],
    "type": "Dinner"   }'

curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2",
   "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2",
    "title": "Egg", 
    "prep_time": 30, 
    "method": "1. Oil on pan\n2.Cook egg on pan\n3. Burn\n4.Cry?\n5. Profit.", 
    "image_url": "https://cookieandkate.com/images/2018/09/crispy-fried-egg-recipe.jpg", 
    "ingredients": ["egg"],
    "type": "Breakfast"   }'

curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
   "firebase_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
    "title": "Potato Chicken", 
    "prep_time": 150, 
    "method": "1. something", 
    "image_url": "https://www.eatwell101.com/wp-content/uploads/2019/11/Garlic-Butter-Mushroom-Skillet-2.jpg", 
    "ingredients": ["potato", "chicken"],
     "type": "Dinner"   }'

 curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
   "firebase_id": "4wYXRpDETSXpkASca8dCOxV5rdh1",
    "title": "Garlic Chicken", 
    "prep_time": 60, 
    "method": "1. Cook Chicken \n2. Eat chicken", 
    "image_url": "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2011/9/1/2/MN0502H_roasted-garlic-clove-chicken_s4x3.jpg.rend.hgtvcom.616.462.suffix/1433073353435.jpeg", 
    "ingredients": ["garlic", "chicken"],
     "type": "Lunch"   }'

curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
   "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
    "title": "Fries", 
    "prep_time": 20, 
    "method": "1. something else", 
    "image_url": "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2012/9/5/1/WU0306H_perfect-french-fries_s4x3.jpg.rend.hgtvcom.616.462.suffix/1589465976850.jpeg", 
    "ingredients": ["potato"],
     "type": "Lunch"   }'

 curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
   "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
    "title": "Tomato Soup", 
    "prep_time": 15, 
    "method": "1. boil tomato in pan", 
    "image_url": "https://www.inspiredtaste.net/wp-content/uploads/2016/08/Tomato-Soup-Recipe-2-1200.jpg", 
    "ingredients": ["tomato"],
     "type": "Breakfast"  }'


 curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
   "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
    "title": "Onion Soup", 
    "prep_time": 125, 
    "method": "1. boil onion in pan", 
    "image_url": "https://www.simplyrecipes.com/thmb/0hC7yNMMKKq3aMKCXMsJMqagy6g=/2880x1920/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-French-Onion-Soup-LEAD-04-c1d3c0e12e2c4a3995bb35d082815f2d.jpg", 
    "ingredients": ["onion"],
     "type": "Breakfast"   }'

     curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": 2,
   "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
    "title": "Mushroom Bhaji", 
    "prep_time": 125, 
    "method": "1. Cook mushroom on stove with mushroom, rice, garlic, tomato", 
    "image_url": "https://www.greedygourmet.com/wp-content/uploads/2019/07/bhajimushroom.jpg", 
    "ingredients": ["potato", "mushroom", "rice", "garlic", "tomato"],
     "type": "Dinner"   }'

    curl -X POST http://127.0.0.1:$1/api/recipes -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{"user_id": 2,
   "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2",
    "title": "Tomato Rice", 
    "prep_time": 125, 
    "method": "1. Rice ketchup haha", 
    "image_url": "https://assets.bonappetit.com/photos/5f315fa5459e181dafb1c526/16:9/w_1280,c_limit/HLY-FMC-Tomato-Rice-16x9.jpg", 
    "ingredients": ["tomato", "rice"],
    "type": "Other"   }'


 curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 1,
    "comment": "Amazing stuff!",
    "rating": 4,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'
curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 1,
    "comment": "MOTHER LOVES THIS RECIPE",
    "rating": 5,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 3,
    "comment": "WOW INCREDIBLE",
    "rating": 3,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'

 curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 2,
    "comment": "Not a fan. Burnt myself :(",
    "rating": 1,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'

  curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 2,
    "comment": "???",
    "rating": 2,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'

  curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 5,
    "comment": "!!!",
    "rating": 2,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'

   curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 3,
    "comment": ":)",
    "rating": 4,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'

   curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 3,
    "comment": ":)",
    "rating": 4,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

   curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 6,
    "comment": ":)",
    "rating": 4,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

  curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 7,
    "comment": ":(",
    "rating": 1,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

   curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 8,
    "comment": ":(",
    "rating": 1,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

  curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 9,
    "comment": ":O",
    "rating": 5,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

 curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 10,
    "comment": ":O",
    "rating": 3,
    "firebase_id": "G8fDMcUtRmQJ2jOT3jw5aE2weTa2"
 }'

  curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 10,
    "comment": "Delicious...",
    "rating": 4,
    "firebase_id": "jYskbOSiNCNaP1xdYohN9Hmn1n52"
 }'

curl -X POST http://127.0.0.1:$1/api/recipes/review -H 'Content-Type: application/json' -H 'Accept: application/json' -d \
 '{ 
    "recipe_id": 10,
    "comment": "SHOOKETH",
    "rating": 3,
    "firebase_id": "W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2"
 }'
fi;
 
# Get recipe through search
#curl -X GET http://127.0.0.1:$1/api/recipes?whitelist=chicken,potato
#curl -X GET http://127.0.0.1:$1/api/recipes?whitelist=chicken&types=Dinner
curl -X GET http://127.0.0.1:$1/api/recipes?sort=ratings


#curl -X GET http://127.0.0.1:$1/api/recipes
#curl -X GET "http://127.0.0.1:$1/api/ingredients/suggest?blacklist=tomato&whitelist=chicken"
