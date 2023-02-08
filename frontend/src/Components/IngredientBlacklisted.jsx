import { ListItemText, MenuItem } from '@mui/material'
import React from 'react'
import UnblacklistIcon from '@mui/icons-material/ArrowUpward';

// Blacklisted ingredient
function IngredientBlacklisted({ingredientFunctions, name, id}) {
  return (
	<MenuItem className="ingredientSelect" idx={id} key={id}>

		<ListItemText primaryTypographyProps={{width: "0px"}}>{name}</ListItemText>
		<UnblacklistIcon color="success" onClick={()=>{
			ingredientFunctions.unblacklistIngredient(name);
			}}/>
	</MenuItem>
  )
}

export default IngredientBlacklisted;
