import React from 'react';
import GoogleIcon from '@mui/icons-material/Google';
import { StoreContext } from '../Utils/store';
import { Button } from '@mui/material';


function Providers() {
	const context = React.useContext(StoreContext);
	const { loginWithGoogle, navigate } = context;

	const providerLogin = async() => {
		try {
				await loginWithGoogle();
				// Login success
				navigate('/profile')
		} catch(err) {
			console.log(err.msg)
		}
	}
  return (
		<div>
			<h2
				style={{
				textAlign: 'center',
				}}
			>
				Or sign in with
			</h2>
			
			<Button variant='outlined' 
			sx={{
				borderRadius: '50%',
				padding: '0',
				width: '50px',
				height: '60px'
			}}
			onClick={providerLogin}>
				<GoogleIcon />
			</Button>


		</div>
  )
}

export default Providers;
