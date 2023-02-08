import React from 'react';
import Button from '@mui/material/Button';
import { StoreContext } from '../Utils/store';
import ProfilePicBtn from './ProfilePicBtn';
import { AppBar, Box } from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';


const appStyle = {
	width: '100vw',
	display: 'flex',
	flexDirection: 'justify',
	color: 'black',
	textAlign: 'center',
	justifyContent: 'space-evenly',
	alignContent: 'space-evenly',
}

const navbarBtn = {
	width: '70px',
	height: '50px',
}



const title = {
	fontWeight: 100, 
	cursor: 'pointer',
	alignContent: 'center',
	textAlign: 'center',
	flexGrow: '65'
}

const start = {
	justifySelf: 'flex-start',
	alignSelf: 'center',
	marginLeft: '50px',
	width: '100px'
}

const end = {
	alignSelf: 'center',
	justifySelf: 'flex-end',
	marginRight: '50px',
	flexGrow: '1'
}

function Navbar() {
	const context = React.useContext(StoreContext);
	const { navigate, currentUser, logout } = context;

	return (
		<Box sx ={{
		borderBottom: '1px solid #dadce0', 
		boxShadow: '0', 
		width: '100%'
		}}>
			<div  style = {appStyle} >
				<div style={start}>
				{currentUser && 
				<Button 
					sx={navbarBtn}
					onClick={()=>{
							logout()
							navigate('/')
					}}
					color='error'
					variant='outlined'><LogoutIcon /></Button> }
				<div></div>

				</div>
				<h1 onClick={() => {
					navigate('/')
				}}
				style={title}>Fantastic Recipes</h1>


				<div style={end}>
					{!currentUser && 
						<Button 
						sx={navbarBtn}
						onClick={()=>{
								navigate('/login')
						}}
						variant='outlined'><LoginIcon/></Button> 
					}
				</div>

				{currentUser && 
					<>

						<div style={end}>
						<ProfilePicBtn/>
						</div>
					
					</>
				}
	
			</div>
		</Box>


	)
}

Navbar.propTypes = {}

export default Navbar
