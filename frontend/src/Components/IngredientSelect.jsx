import { Checkbox, ListItemText, MenuItem } from '@mui/material'
import React, { useEffect } from 'react'
import BlackListIcon from '@mui/icons-material/DeleteOutline';
import { useState } from 'react';

/*
	Component for individual ingredient select
	Page: Home
*/
function IngredientSelect({changeSearchText, suggested, changeSuggested, ingredientFunctions, name, id}) {
  const [menuStyle, setMenuStyle] = useState({background: "white"});

 

  useEffect(() => {
	if(suggested && suggested === name) {
		setMenuStyle({background: "#76d3fe",});
	} else {
		setMenuStyle({background: "white"});
	}
  }, [suggested])
  return (
	  <MenuItem  sx={menuStyle} className="ingredientSelect" idx={id} key={id}>
		<Checkbox value={name} onClick={(e) => {
		  if(e.target.checked)
			ingredientFunctions.addIngredient(e.target.value)
		  else
			ingredientFunctions.removeIngredient(e.target.value)
		  changeSuggested(null);
		  changeSearchText('');
		  
		  }}></Checkbox>
		<ListItemText primaryTypographyProps={{width: "0px"}}>{name}</ListItemText>
		<BlackListIcon color="error" onClick={(e) => {
		  ingredientFunctions.blacklistIngredient(name);
		  changeSuggested(null, !e.target.checked);

		  }}/>
	  </MenuItem>
	)
}


export default IngredientSelect
