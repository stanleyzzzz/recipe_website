import React, { useState } from 'react';
import Chatbot from '../../Components/Chatbot';
import IngredientsSidebar from '../../Components/IngredientsSidebar';
import Navbar from '../../Components/Navbar';
import RecipeCards from '../../Components/RecipeCards';
import './styles.scss';

function Home() {
	// Ingredients
	const [selectedIngredients, setSelectedIngredients] = useState([]);
	const [blacklistedIngredients, setBlacklistedIngredients] = useState([]);
	const [mealTypes, setMealTypes] = useState([]);
	const [sort, setSort] = React.useState("ratings");
	

	// Adding ingredients through checkbox
	const addIngredient = (ingredient) => {
		setSelectedIngredients(selectedIngredients => [...selectedIngredients, ingredient])
	}

	// Remove ingredients
	const removeIngredient = (ingredient) => {
		setSelectedIngredients(current =>
			current.filter(name => {
				return name !== ingredient;
			}),
			);
	}
	
	// Blacklisting ingredients through bin icon
	const blacklistIngredient = (ingredient) => {
		setBlacklistedIngredients(blacklistedIngredients => [...blacklistedIngredients, ingredient])

		// have to remove from selected ingredients when blacklisted
		setSelectedIngredients(current =>
			current.filter(name => {
				return name !== ingredient;
			}),
			);
	}

	// Remove ingredients from blacklist
	const unblacklistIngredient = (ingredient) => {
		setBlacklistedIngredients(current =>
			current.filter(name => {
				return name !== ingredient;
			}),
		);
	}

	// Add meal type
	const addMealType = (mealType) => {
		setMealTypes(selectedMealTypes => [...selectedMealTypes, mealType])
	}

	// Remove meal type
	const removeMealType = (mealType) => {
		setMealTypes(current =>
			current.filter(name => {
				return name !== mealType;
			})
		);
	}
	

	// get selected ingredients
	const getSelected = () => {
		return selectedIngredients;
	}

	// get blacklisted ingredients
	const getBlacklisted = () => {
		return blacklistedIngredients;
	}

	// get meal type
	const getMealType = () => {
		return mealTypes;
	}

	const resetFilters = () => {
		setSelectedIngredients([]);
		setMealTypes([]);
		setBlacklistedIngredients([])
	}

	// Functions for ingredients, passing down to child components
	const ingredientFunctions = {
		removeIngredient: removeIngredient,
		addIngredient: addIngredient,
		getSelected: getSelected,
		blacklistIngredient: blacklistIngredient,
		unblacklistIngredient: unblacklistIngredient,
		getBlacklisted: getBlacklisted,
		addMealType: addMealType,
		removeMealType: removeMealType,
		getMealType: getMealType,
		resetFilters: resetFilters
	}

	return (
		<>
			<Navbar></Navbar>
			<div className="homeWrapper">
				<IngredientsSidebar ingredientFunctions={ingredientFunctions}/>
				<RecipeCards 
				mealTypes={mealTypes}
				selectedIngredients={selectedIngredients} 
				blacklistedIngredients={blacklistedIngredients}
				sort={sort}
				setSort={setSort}
				/>
			</div>
			<Chatbot/>
		</>
	)
}

export default Home;
