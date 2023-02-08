import { Box } from '@mui/system'
import React from 'react'
import IngredientBlacklisted from './IngredientBlacklisted'


/*
	TODO 
*/
function Blacklist({ingredients, ingredientFunctions}) {
	return (
		<div>
			<h3>Blacklist</h3>
			<Box className="ingredientListWrapper">
				<Box className="ingredientListBox  blacklist">
				{ingredients.map((ing) => {
					if(ingredientFunctions.getBlacklisted().includes(ing)) {
						return (<IngredientBlacklisted 
						ingredientFunctions={ingredientFunctions}
						name={ing} 
						key={ing}
						/>)
					}
					
				})}

			
			</Box>
		</Box>
		
		</div>
		
	)
}

export default Blacklist
