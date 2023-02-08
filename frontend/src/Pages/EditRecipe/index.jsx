import { Button, Card, CircularProgress } from '@mui/material'
import React, { useState } from 'react'
import StarRatings from 'react-star-ratings';
import { deleteData, getData, postData, updateData } from '../../Helpers/helpers';
import { StoreContext } from '../../Utils/store';
import DeleteIcon from '@mui/icons-material/Delete';
import { Navigate, useParams } from 'react-router';
import Navbar from '../../Components/Navbar';
import './styles.scss';

function EditRecipe() {
	const context = React.useContext(StoreContext)
	const { currentUser, navigate } = context;
    const { i } = useParams();
	const [recipesList, setRecipesList] = useState([]);
	const [recipe, setRecipe] = useState(null);
	const [isAdding, setIsAdding] = useState(false);
	const [loading, setLoading] = useState(true);
  
    
      const editRecipe = (i) => {
        const recipe = recipesList[0];
        // TODO: edit ingredient when bacckend route allows for it
        // ingredients: recipe.ingredients.split(', ') 
        updateData(`http://localhost:8080/api/recipes/${recipe.recipe_id}`, { 
			firebase_id: currentUser.id, 
			title: recipe.title, 
			prep_time: recipe.prep_time, 
			method: recipe.method, 
			image_url: recipe.image })
          .then(data => {
			
            fetchRecipes();
			alert("Recipe has been saved!")
			navigate("/profile/recipes")
          })
          .catch(err => {
			alert("Recipe was not saved!")

          })
      }
    
      const deleteRecipe = (id) => {
		let confirmDelete = window.confirm("Are you sure to delete this recipe? You will not be able to retrieve it.");
		if(confirmDelete) {
			deleteData(`http://localhost:8080/api/recipes/${id}`, { requesting_user_id: currentUser.id })
			.then(data => {
				alert("Recipe has been deleted!")
				navigate("/profile/recipes")
			})
			.catch(err => {
				console.log(err);
			})
	 	 }
		 else {
			alert("Recipe was not deleted!");
		 }
      }

    // fetch current user's recipes
	const fetchRecipes = React.useCallback(() => {
		if(currentUser) {
			getData(`http://localhost:8080/api/recipes/user/${currentUser.id}`)
			.then(res => {
				return res.json()
			})
			.then(data => {

				setRecipesList(data.recipes.filter((a) => a.recipe_id === parseInt(i)));
			})
			.catch(err => console.error(err));
		}
    }, [currentUser]);


			

			React.useEffect(() => {
				fetchRecipes();
				setLoading(false)
				console.log("using state!")
			}, []);
      
		
		if(loading) {
			return <CircularProgress/>;
		}
			
		if(recipesList.length < 1) {
			return <Navbar/>
		}

		return (
			<>
			<Navbar/>
			<h1>Edit Recipes</h1>
			<Card key={recipesList[0].recipe_id} className="recipesBoxCard">
					<div className="recipesBoxCardName">
						Name:&nbsp;&nbsp;
						<input type="text" value={recipesList[0].title} onChange={(e) => setRecipesList(pre => [{ ...pre[0], title: e.target.value }])} />
					</div>
					<div className="recipesBoxCardImage">
						Image:&nbsp;&nbsp;
						<input type="text" value={recipesList[0].image} onChange={(e) => setRecipesList(pre => [{ ...pre[0], image: e.target.value }])} />
					</div>
					<div className="recipesBoxImg" 
						alt={`${recipesList[0].name}`}
					 	style={{backgroundImage: "url('" + recipesList[0].image + "')"}}>

					</div>
					<div className="recipesBoxCardMethods">
						Methods:&nbsp;&nbsp;
						<br />
						<textarea type="text" value={recipesList[0].method} onChange={(e) => setRecipesList(pre => [{ ...pre[0], method: e.target.value }])} />
					</div>
					{/*
					<div className="recipesBoxCardIngredients">
						Ingredients:&nbsp;&nbsp;
						<input type="text" value={recipesList[0].ingredients.join(', ')} onChange={(e) => setRecipesList(pre => [{ ...pre[0], ingredients: e.target.value.split(', ') }])} />
					</div>
			*/}
					<div className="recipesBoxCardTime">
						Time to cook:&nbsp;&nbsp;
						<input type="number" value={recipesList[0].prep_time} onChange={(e) => setRecipesList(pre => [{ ...pre[0], prep_time: e.target.value }])} />
						&nbsp;minutes
					</div>
					
					<div className="options">
						<Button
						onClick={() => editRecipe(i)}
						color='success' variant="contained">
						Save
						</Button>
						<DeleteIcon onClick={() => deleteRecipe(recipesList[0].recipe_id)} fontSize='large' className="deleteIcon" />
					</div>
					</Card>
			</>
		)
}

export default EditRecipe
