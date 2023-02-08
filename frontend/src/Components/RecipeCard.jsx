import { Card, CardActionArea, CardActions, CardContent, CardHeader, CardMedia, CircularProgress, Rating, Typography } from '@mui/material'
import React, { useState } from 'react'
import { StoreContext } from '../Utils/store';
import FaceIcon from '@mui/icons-material/Face';
import { useEffect } from 'react';
import { getData } from '../Helpers/helpers';



// Change this depending on what data we get
function RecipeCard({recipe, isUserRecipe}) {
	const context = React.useContext(StoreContext);
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);


	useEffect(() => {
		const getUser = async() => {
			//console.log(recipe)

			// TODO
			// Fix this once backend works

			// Right now this gets all the users based off of the admin
			//const res = await getData("http://127.0.0.1:8080/api/users/list/W7Mg7D3tJuUcTo0nbq2XvLO2Q2z2");
			//const data = await res.json();
			//let users = data["users"];
			//console.log(users)
			//let u = users.filter((a)=>{ return a.user_id === recipe.user_id})[0]
			//setUser(u)

			setLoading(false);
		}
		getUser();
	},[recipe])

	
 	const { navigate } = context;
	if(loading) {
		return <CircularProgress/>;
	}
	return (

			<Card className="recipeCard" key={recipe.recipe_id}>
				<CardActionArea onClick={()=>{
					if(!isUserRecipe)
						navigate('/recipe/' + recipe.recipe_id)
					else 
						navigate('/recipe/edit/' + recipe.recipe_id)
					
					}}>
			
					<CardHeader
						title={recipe.title}
						subheader={<> {recipe.prep_time + " minutes | " + recipe.no_reviews + " reviews"}</>}
						titleTypographyProps={{variant:'p', fontSize: "20px", fontWeight: "bolder" }}
						subheaderTypographyProps={{fontSize: "12px", fontWeight: "light"}}

					>
					</CardHeader>
					
					<CardMedia
					component="img"
					height="120"
					image={recipe.image}
					alt={"image of " + recipe.title}
					></CardMedia>

					<CardContent>
						{/*TODO RATINGS */}
						<Rating name="read-only" value={recipe.ratings} readOnly precision={0.5}/>
					</CardContent>
					<CardActions>
						More...
					</CardActions>
				</CardActionArea>
			</Card>
	)
}

export default RecipeCard
