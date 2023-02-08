import React from 'react'
import { StoreContext } from '../Utils/store'
import { Route, Routes } from 'react-router';

import Register from './Register';
import Login from './Login'
import Home from './Home';
import Profile from './Profile';
import AdminDashboard from './AdminDashboard';
import UserRecipes from './UserRecipes';
import Recipe from './Recipe';
import HomeBtn from '../Components/HomeBtn'
import EditRecipe from './EditRecipe';
// Page for dealing with the routes of the application
// TODO prevent unauthorised users from accessing protected pages

function PageRoutes(props) {
	const context = React.useContext(StoreContext);

	return (
		<div>
			<Routes>
				<Route exact path="/" element={<Home/>}></Route>
				<Route exact path="/register" element={<Register />}></Route>
				<Route exact path="/login" element={<Login/>}></Route>
        		<Route exact path="/recipe/:id" element={<Recipe />}></Route>
        		<Route exact path="/recipe/edit/:i" element={<EditRecipe/>}></Route>
				<Route exact path="/profile/" element={<Profile/>}></Route>
        		<Route exact path="/profile/recipes" element={<UserRecipes />}></Route>
        		<Route exact path="/admin/dashboard/" element={<AdminDashboard />}></Route>
				<Route path="*" element={<><HomeBtn/> <h1>404 Page not found</h1></>}></Route>
			</Routes>
		</div>
	)
}

export default PageRoutes
