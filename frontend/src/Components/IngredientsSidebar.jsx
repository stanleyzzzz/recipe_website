import { Box, Button, CircularProgress, IconButton, InputAdornment, TextField } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { StoreContext } from '../Utils/store';
import IngredientsList from './IngredientsList';
import SearchIcon from '@mui/icons-material/Search';
import Blacklist from './Blacklist';
import { getData } from '../Helpers/helpers';
import MealTypeList from './MealTypeList';
import ResetIcon from '@mui/icons-material/RestartAlt';
/*
	Component for the ingredients sidebar with search and suggestions
	Page: Home
*/
function IngredientsSidebar({ ingredientFunctions }) {
    const context = React.useContext(StoreContext);

	// Searching in ingredients text
	const [searchText, setSearchText] = useState('');

	// For async
	const [loading, setLoading] = useState(false); // Set to true when backend complete
	const [ingredients, setIngredients] = useState([]);
	const [suggested, setSuggested] = useState(null);
	const [suggestDisabled, setSuggestDisabled] = useState(true);


	// Getting the ingredients array data from backend API
	const getIngredients = async() => {
		const res = await getData("http://127.0.0.1:8080/api/ingredients");
		const data = await res.json();
		setLoading(false);
		setIngredients(data.ingredients);
	}

	useEffect(() => {
		
		getIngredients();
	}, []);

	
	// Changes search text
	const changeSearchText= (text) => {
		setSearchText(text);
	}

	// Changes the suggested 
	const changeSuggested = (ingredient) => {
		setSuggested(ingredient);
		setSuggestDisabled(false);
		if(ingredient !== null) {
			changeSearchText(ingredient)
		}
	}

	// Get a suggestion based on blacklist and whitelist
	const getSuggestion = async() => {
		let black = "";
		let white = "";
		let types = "";

		// probably a better way to do this
		let selectedIngredients = ingredientFunctions.getSelected();
		for(const ing in  selectedIngredients) {
			white += selectedIngredients[ing]
		}
			
		let blacklistedIngredients = ingredientFunctions.getBlacklisted();
		for(const ing in blacklistedIngredients) {
			black += blacklistedIngredients[ing]+","
		}

		let mealTypes = ingredientFunctions.getMealType();
		for(const i in mealTypes) {
			types += mealTypes[i]+","
		}
		// empty whitelist will change results
		let res = null; 

		if(selectedIngredients.length > 0) {
			res = await getData("http://127.0.0.1:8080/api/ingredients/suggest?blacklist="+black+"&whitelist="+white+"&types="+types);
		}
		else {
			res = await getData("http://127.0.0.1:8080/api/ingredients/suggest?blacklist="+black+"&types="+types);
		}
		
		const data = await res.json();

		if(data.code === 500 || !data.ingredient) {
			alert("No suggestions available!");
			console.log(data)
			setSuggestDisabled(true);
			return;
		}

		// Keep this for now, suggestion is incomplete
		// TODO fix this
		console.log(data); 
		changeSuggested(data.ingredient);
	}

	
	if(loading) {
		return <CircularProgress />;
	}
	
	return (
		<Box className="sidebarWrapper">
			<Box  className="sidebar">
				<h3 onClick={()=>{console.log(ingredientFunctions.getMealType())}}>Ingredients Search</h3>
				<Box className="ingredientSearchBarWrapper">
					<TextField 
						placeholder="Search Ingredients"
						className="ingredientSearchBar"
						value={searchText}
						onChange={(e) => {
								setSearchText(e.target.value)
							}}
						InputProps={{
							endAdornment: (
							<InputAdornment position="end">
								<IconButton edge="end" color="primary">
									<SearchIcon />
								</IconButton>
							</InputAdornment>
							),
						}}
					></TextField>
				</Box>

				<Button className="suggestionModeBtn" 
				disabled={suggestDisabled} 
				variant="outlined"
				onClick={() => {getSuggestion()}}
				>Suggestion</Button>

				<Button className="resetBtn" 
				color="warning"
				variant="outlined"
				onClick={() => {
					ingredientFunctions.resetFilters()
					window.location.reload(false);
				}}
				><ResetIcon/></Button>


					
				
	
				<IngredientsList changeSearchText={changeSearchText}  changeSuggested={changeSuggested} suggested={suggested} ingredientFunctions={ingredientFunctions} searchText={searchText} ingredients={ingredients}/>
			
				<Blacklist ingredientFunctions={ingredientFunctions} ingredients={ingredients}/>
				<MealTypeList ingredientFunctions={ingredientFunctions}/>
				<div style={{height: "100px"}}></div>
			</Box>
		</Box>

	)
}

export default IngredientsSidebar
