import { Card, FormControl, InputLabel, Select, TextField } from '@mui/material'
import React, { useState, useEffect } from 'react'
// import { data } from './dummy'
import { getData } from '../Helpers/helpers'
import RecipeCard from './RecipeCard'
import SortByMenu from './SortByMenu'


function RecipeCards({ selectedIngredients, blacklistedIngredients, mealTypes, sort, setSort }) {

	const [loading, setLoading] = useState(false) // set to true when backend is complete
	const [recipes, setRecipes] = useState([])


	// Search text
	const [recipeSearchText, setRecipeSearchText] = useState("");

	// Function for filtering recipes
	
	const filterRecipes = (recipeIngredients) => {
		// if there are no ingredients selected, show all
		if(selectedIngredients.length === 0) {
			return blacklistedIngredients.every(val => !recipeIngredients.includes(val));
		}


		// if ingredients are selected, show recipe name search
		//  + recipes with selected ingredients
		return selectedIngredients.every(val => recipeIngredients.includes(val)) &&
		blacklistedIngredients.every(val => !recipeIngredients.includes(val));
	}

	useEffect(() => {
		// Getting the recipes array data from backend API
		const getRecipes = async() => {
			let black = "";
			let white = "";
			let types = "";
			
			for(const i in selectedIngredients) {
				white += selectedIngredients[i]+","
			}
			white = white.slice(0, -1);
		
			for(const i in blacklistedIngredients) {
				black += blacklistedIngredients[i]+","
			}
			black = black.slice(0, -1);

			for(const i in mealTypes) {
				types += mealTypes[i]+","
			}
			types = types.slice(0, -1);

	
			if(white.length === 0) {
				const res =  await getData("http://127.0.0.1:8080/api/recipes?name="+recipeSearchText+"&blacklist="+black+"&types="+types+"&sort="+sort);
				const data = await res.json();
				setLoading(false);
				setRecipes(data);
			} else {
				const res =  await getData("http://127.0.0.1:8080/api/recipes?name="+recipeSearchText+"&blacklist="+black+"&whitelist="+white+"&types="+types+"&sort="+sort);
				const data = await res.json();
				setLoading(false);
				setRecipes(data);
			}
			
			// setRecipes(data.recipes.filter((recipe) => filterRecipes(recipe.name, recipe.ingredients)));
			// console.log(recipes.length)
		}

		const getRecipe = () => {
			// const res = getData("https://localhost:3000/api/recipes/" + recipeId);
			//const data = res.json();
			// setLoading(false);
			// setRecipes(data.recipes);
		}


		// TODO
		// Use once backend API route for /api/recipes has been completed 
		getRecipes();
	}, [selectedIngredients, blacklistedIngredients, mealTypes, sort, recipeSearchText]);

	if(loading) {
		return <>Loading recipes...</>;
	} 

	if(recipes.length < 1) {
		
		return 		(<div className="recipeSection">
						<div className="searchSection">
						<TextField 
							placeholder="Search recipes"
							variant="standard" 
							className="recipeSearchBar"
							onChange={(e)=> setRecipeSearchText(e.target.value)}
							></TextField>
							<SortByMenu sort={sort} setSort={setSort}/>
						</div>
							<h3>No recipes matching your result!</h3>
					</div>)
	}
	return (
		<div className="recipeSection">
				<div className="searchSection"> 
					<TextField 
					placeholder="Search recipes"
					variant="standard" 
					className="recipeSearchBar"
					onChange={(e)=> setRecipeSearchText(e.target.value)}
					></TextField>
					<SortByMenu sort={sort} setSort={setSort}/>
				</div>
				<div className="recipeCards">
					
					 {	
					 	// TODO
					 	// remove data. once backend is complete 
						// mapping out the data
						recipes.map((recipe, i) => {
							
								return (
								<>
								<RecipeCard recipe={recipe} id={i} isUserRecipe={false}/>
								</>)
							
							
						})
					 }
				</div>
		</div>
	)
}

export default RecipeCards
