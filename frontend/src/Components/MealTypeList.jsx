import { Box } from '@mui/system'
import React, { useState } from 'react'
import MealTypeSelect from './MealTypeSelect'

function MealTypeList({ingredientFunctions}) {

	const [mealTypes] = useState(["Breakfast", "Lunch", "Dinner", "Drinks", "Other"])
	return (
		<div>
			<h3>Meal Types</h3>
		<Box  className="ingredientListWrapper">
			<Box className="ingredientListBox mealTypes">

				{
				mealTypes.map((mealType, id) => {
						return (
							<MealTypeSelect ingredientFunctions={ingredientFunctions} name={mealType} id={id}/>
						)
					})
				}
				
			</Box>
		</Box>
		</div>
  	)
}

export default MealTypeList
