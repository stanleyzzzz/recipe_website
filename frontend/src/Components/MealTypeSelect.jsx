import { Checkbox, ListItemText, MenuItem } from '@mui/material';
import React from 'react'

function MealTypeSelect({ingredientFunctions, name, id}) {


  return (
	<MenuItem idx = {id} className="ingredientSelect">
		<Checkbox value={name} 
		onClick={(e)=>{
			if(e.target.checked)
				ingredientFunctions.addMealType(e.target.value)
		  	else
				ingredientFunctions.removeMealType(e.target.value)

		}}></Checkbox>
		<ListItemText primaryTypographyProps={{width: "0px"}}>{name}</ListItemText>
  	</MenuItem>
  )
}

export default MealTypeSelect
