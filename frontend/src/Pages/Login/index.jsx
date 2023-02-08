import { Alert, AlertTitle, Box, Button, Collapse, TextField } from '@mui/material';
import React, { useState } from 'react';
import HomeBtn from '../../Components/HomeBtn';
import Providers from '../../Components/Providers';
import { getData } from '../../Helpers/helpers';
import { StoreContext } from '../../Utils/store';
import './styles.scss';


/* 
	Basic login through firebase using email + password
	or Google Authentication
*/
function Login() {
	const context = React.useContext(StoreContext);

	// TextField data
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	// For highlighting TextFields 
	const [emailErr, setEmailErr] = useState(false);
	const [passwordErr, setPasswordErr] = useState(false)

	const [emailErrText, setEmailErrText] = useState('');
	const [passwordErrText, setPasswordErrText] = useState('')

	const [isOpen, setIsOpen] = useState(false)

	const { login, navigate, setUserDetails, currentUser, userDetails } = context;

	// Highlights the TextField if empty, otherwise doesn't
	const checkInput = () => {
		if(email.length < 1) {
			setEmailErr(true);
			setEmailErrText('Email field cannot be empty.');
		}
		else {
			setEmailErr(false);
			setEmailErrText('');

		}

		if(password.length < 1) {
			setPasswordErr(true);
			setPasswordErrText('Password field cannot be empty.');
		}
		else {
			setPasswordErr(false);
			setPasswordErrText('');
		}
	}

	// Basic login with email and password through Firebase
	const loginWithEmailAndPass = async() => {
		checkInput();
		
		try {
			let loginDetails = await login(email, password);

			let data = await getData(`http://localhost:8080/api/users/${loginDetails.user.uid}`)
			let user = await data.json();
			console.log(user)

			if(user.is_banned) {
				setIsOpen(true);
			} else {
				navigate('/profile')
			}
			// Login Success
			//
		} catch (err) {
			// Login Failures
			console.error(err);
		
			
			setEmailErr(true);
			setEmailErrText('Email or password is incorrect.');
			// alert(err.message);
		}
	}


	React.useEffect(() => {
	}, []);

	return (
	<>
		<Collapse in={isOpen}>
			<Alert sx={{position: "relative"}}
			severity="error"
			onClose={() => {
				setIsOpen(false);
			}}>
				<AlertTitle>You have been banned.</AlertTitle>
				One of our admins have banned you from this website. You do not have access to your account.
			</Alert>
		</Collapse>
		<HomeBtn/>
	
		<div className = 'wrapper'>
		
			<Box className = 'loginBox'>
				<h1> Login </h1>
				<TextField 
					helperText={emailErrText}
					error={emailErr}
					onChange={(e)=>{
						setEmail(e.target.value)
					}}
				id="filled-basic" label="Email" variant="filled" />
				<br></br>
				<TextField 
					helperText={passwordErrText}
					error={passwordErrText}
					onChange={(e)=>{
						setPassword(e.target.value)
					}}
				id="filled-basic" label="Password" variant="filled" type="password" />
	
			<br></br>
			<div className = 'loginButtons'>
				<Button variant="outlined" 
				onClick={()=>{
					navigate('/register')
				}}>Register</Button>

				<Button variant="contained" 
				onClick={loginWithEmailAndPass}>Log in</Button>
			</div>

			<br></br>
			<Providers></Providers>
		</Box>
	</div>

	</>
	)
}

export default Login;
