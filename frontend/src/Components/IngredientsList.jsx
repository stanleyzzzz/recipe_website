import { Box } from '@mui/material'
import React from 'react'
import IngredientSelect from './IngredientSelect'

/*
	Component for mapping ingredient select
	Page: Home
*/
function IngredientsList({ changeSearchText, suggested, changeSuggested, ingredientFunctions, ingredients, searchText }) {
	
	
	// Filter the ingredients based on their name
	// Ensure not to include any blacklisted items
	const filterIngredients = (name) => {
		return (name.includes(searchText) 
		|| ingredientFunctions.getSelected().includes(name))
		&& !ingredientFunctions.getBlacklisted().includes(name);
	}
	
	return (
		<Box className="ingredientListWrapper">
			<Box className="ingredientListBox">
				{ingredients.map((ing) => {
					if(filterIngredients(ing)) {
						return (<IngredientSelect 
						changeSearchText={changeSearchText}
						changeSuggested={changeSuggested}
						suggested={suggested}
						ingredientFunctions={ingredientFunctions}
						name={ing} 
						/>)
					}
					
				})}

			
			</Box>
		</Box>
  )
}

export default IngredientsList
