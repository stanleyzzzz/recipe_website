import { Box, Card, Button, FormControl, MenuItem, Select, InputLabel } from '@mui/material';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import StarRatings from 'react-star-ratings';
import Navbar from '../../Components/Navbar';
import React, { useState } from 'react';
import { getData, postData, deleteData, updateData } from '../../Helpers/helpers.jsx';
import { StoreContext } from '../../Utils/store';
import DeleteIcon from '@mui/icons-material/Delete';
import './styles.scss';
import RecipeCard from '../../Components/RecipeCard';

/*
 * User's dashboard that allows them to view, edit, delete, add recipes
*/

function UserRecipes() {
	const context = React.useContext(StoreContext);
	const { currentUser } = context;

  const [recipesList, setRecipesList] = useState([]);
  const [isAdding, setIsAdding] = useState(false);
  const [newRecipe, setNewRecipe] = useState({ name: '', methods: '', image: '', time: 0, ingredients: '', type: "Breakfast" });
  const [newRecipeFreqIngredients, setNewRecipeFreqIngredients] = useState([]);

  // fetch current user's recipes
	const fetchRecipes = React.useCallback(() => {
    getData(`http://localhost:8080/api/recipes/user/${currentUser.id}`)
      .then(res => {
        return res.json()
      })
      .then(data => {
        setRecipesList(data.recipes);
      })
      .catch(err => console.error(err));
	}, [currentUser.id]);

  const getFreqIngredients = () => {
    getData(`http://localhost:8080/api/ingredients/frequent_ingredients`)
      .then(res => res.json())
      .then(data => setNewRecipeFreqIngredients(data.ingredients_without_recipe))
      .catch(err => console.error(err));
  }

  const addRecipe = () => {
    postData(`http://localhost:8080/api/recipes`, { firebase_id: currentUser.id, title: newRecipe.name, prep_time: newRecipe.time, method: newRecipe.methods, image_url: newRecipe.image, ingredients: newRecipe.ingredients.split(', '), type: newRecipe.type })
      .then(data => {
        setIsAdding(false);
        setNewRecipe({ name: '', methods: '', image: '', time: 0, ingredients: '' });
        fetchRecipes();
      })
      .catch(err => {
        console.log(err);
        setIsAdding(false);
      })
  }

  const editRecipe = (i) => {
    const recipe = recipesList[i];
    updateData(`http://localhost:8080/api/recipes/${recipe.recipe_id}`, { firebase_id: currentUser.id, title: recipe.title, prep_time: recipe.prep_time, method: recipe.method, image_url: recipe.image })
      .then(data => {
        fetchRecipes();
      })
      .catch(err => {
        console.log(err);
      })
  }

  const deleteRecipe = (id) => {
    deleteData(`http://localhost:8080/api/recipes/${id}`, { requesting_user_id: currentUser.id })
      .then(data => {
        fetchRecipes();
      })
      .catch(err => {
        console.log(err);
      })
  }

	React.useEffect(() => {
    fetchRecipes();
	}, [fetchRecipes]);

	return (
    <>
      <Navbar />
      <div className="userDashboardWrapper">
        <h1 className="shadowTxt">My Recipes</h1>
        <Button
          onClick={() => {
            getFreqIngredients();
            setIsAdding(true);
          }}
          color='secondary' variant="contained">
          Add Recipe
        </Button>
        <Box className="recipesBox">
          {!recipesList.length && "You have no recipes"}
          {recipesList.map((recipe, i) => (
            <RecipeCard recipe={recipe} id={i} isUserRecipe={true}/>
          ))}
        </Box>
      </div>
      <Dialog open={isAdding} onClose={() => setIsAdding(false)}>
        <DialogTitle>Add Recipe</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <b>Frequent ingredients without a recipe</b>
            <br />
            {newRecipeFreqIngredients.join(", ")}
          </DialogContentText>
          <TextField
            autoFocus
            margin="normal"
            label="Recipe Name"
            type="text"
            value={newRecipe.name}
            onChange={(e) => setNewRecipe(pre => ({...pre, name: e.target.value}))}
            fullWidth
            variant="standard"
          />
           <FormControl variant="standard" sx={{width: 120}}>
                <InputLabel id="demo-simple-select-standard-label">Meal Type</InputLabel>
                  <Select
                    labelId="demo-simple-select-standard-label"
                    id="demo-simple-select-standard"
                    value={newRecipe.type}
                    onChange={(e)=>{
                      setNewRecipe(pre => ({...pre, type: e.target.value}))
                    }}
                    label="Meal Type"
                  >
                    
                  <MenuItem value={"Breakfast"}>Breakfast</MenuItem>
                  <MenuItem value={"Lunch"}>Lunch</MenuItem>
                  <MenuItem value={"Dinner"}>Dinner</MenuItem>
                  <MenuItem value={"Drinks"}>Drinks</MenuItem>
                  <MenuItem value={"Other"}>Other</MenuItem>

                </Select>
              </FormControl>
          <TextField
            margin="normal"
            label="Methods"
            type="text"
            value={newRecipe.methods}
            onChange={(e) => setNewRecipe(pre => ({...pre, methods: e.target.value}))}
            fullWidth
            variant="standard"
            multiline
            rows={6}
          />
          <TextField
            margin="normal"
            label="Image"
            type="text"
            value={newRecipe.image}
            onChange={(e) => setNewRecipe(pre => ({...pre, image: e.target.value}))}
            fullWidth
            variant="standard"
          />
          <img src={newRecipe.image} alt={newRecipe.name} style={{ maxWidth: '500px' }} />
          <TextField
            margin="normal"
            label="Recipe time (mins)"
            type="number"
            value={newRecipe.time}
            onChange={(e) => setNewRecipe(pre => ({...pre, time: e.target.value}))}
            fullWidth
            variant="standard"
          />
          <TextField
            margin="normal"
            label="Ingredients (egg, pork, beef)"
            type="text"
            value={newRecipe.ingredients}
            onChange={(e) => setNewRecipe(pre => ({...pre, ingredients: e.target.value}))}
            fullWidth
            variant="standard"
          />
           
              </DialogContent>
              <DialogActions>

          <Button onClick={() => setIsAdding(false)}>Cancel</Button>
          <Button onClick={addRecipe}>Submit</Button>
        </DialogActions>
      </Dialog>
    </>
	)
}

export default UserRecipes;
