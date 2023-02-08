import { Box, Button, TextField } from '@mui/material';
import React, { useState } from 'react';
import Providers from '../../Components/Providers';
import { StoreContext } from '../../Utils/store';
import './styles.scss';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

/*
	Basic registration through firebase using email + password
	or Google Authentication
*/
function Register() {
	const context = React.useContext(StoreContext);

	// TextField data
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [firstName, setFirstName] = useState('');
	const [lastName, setLastName] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');

	// For highlighting TextFields
	const [emailErr, setEmailErr] = useState(false);
	const [usernameErr, setUsernameErr] = useState(false);
	const [firstNameErr, setFirstNameErr] = useState(false)
	const [lastNameErr, setLastNameErr] = useState(false)
	const [passwordErr, setPasswordErr] = useState(false)
	const [confirmPasswordErr, setConfirmPasswordErr] = useState(false)

	const [emailErrText, setEmailErrText] = useState('');
	const [usernameErrText, setUsernameErrText] = useState('');
	const [firstNameErrText, setFirstNameErrText] = useState('');
	const [lastNameErrText, setLastNameErrText] = useState('');
	const [passwordErrText, setPasswordErrText] = useState('')
	const [confirmPasswordErrText, setConfirmPasswordErrText] = useState('');

	const { register, navigate } = context;

	// Highlights the TextField if empty, otherwise doesn't
	const checkInput = () => {
		if (email.length < 1) {
			setEmailErr(true);
			setEmailErrText('Email field cannot be empty.');
		} else {
			setEmailErr(false);
			setEmailErrText('');
		}

		if (password.length < 1) {
			setPasswordErr(true);
			setPasswordErrText('Password field cannot be empty.');
		} else {
			setPasswordErr(false);
			setPasswordErrText('');
		}

		if (username.length < 1) {
			setUsernameErr(true);
			setUsernameErrText('Username field cannot be empty.');
		} else {
			setUsernameErr(false);
			setUsernameErrText('');
		}

		if (firstName.length < 1) {
			setFirstNameErr(true);
			setFirstNameErrText('Firstname field cannot be empty.');
		} else {
			setFirstNameErr(false);
			setFirstNameErrText('');
		}

		if (lastName.length < 1) {
			setLastNameErr(true);
			setLastNameErrText('Lastname field cannot be empty.');
		} else {
			setLastNameErr(false);
			setLastNameErrText('');
		}

    if (confirmPassword !== password) {
      setPasswordErr(true);
      setConfirmPasswordErr(true);
      setConfirmPasswordErrText('Password must match confirm password.');
    } else {
      setPasswordErr(false);
      setConfirmPasswordErr(false);
    }
	}

	// Basic register with email and password through Firebase
	const signupWithEmailAndPass = async() => {
		checkInput();

		try {
			await register(email, username, firstName, lastName, password);
			// signup Success
			navigate('/');
		} catch (err) {
			// signup Failures
			console.error(err);

			setEmailErr(true);
			setEmailErrText('Email is in use.');
		}
	}


	React.useEffect(() => {
	}, []);

	return (
	<>
		{
		// Should this be a component???
		}
		<Button onClick={()=>{
			navigate('/')
		}}>
			<ArrowBackIcon></ArrowBackIcon>
			Return Home
		</Button>

		<div className = 'wrapper'>
			<Box className = 'signupBox'>
				<h1> Sign Up</h1>
				<TextField
					helperText={emailErrText}
					error={emailErr}
					onChange={(e)=>{
						setEmail(e.target.value)
					}}
				id="filled-basic" label="Email" variant="filled" />
				<br></br>
				<TextField
					helperText={usernameErrText}
					error={usernameErr}
					onChange={(e)=>{
						setUsername(e.target.value)
					}}
				id="filled-basic" label="Username" variant="filled" />
				<br></br>
				<TextField
					helperText={firstNameErrText}
					error={firstNameErr}
					onChange={(e)=>{
						setFirstName(e.target.value)
					}}
				id="filled-basic" label="First Name" variant="filled" />
				<br></br>
				<TextField
					helperText={lastNameErrText}
					error={lastNameErr}
					onChange={(e)=>{
						setLastName(e.target.value)
					}}
				id="filled-basic" label="Last Name" variant="filled" />
				<br></br>
				<TextField
					helperText={passwordErrText}
					error={passwordErr}
					onChange={(e)=>{
						setPassword(e.target.value)
					}}
				id="filled-basic" label="Password" variant="filled" type="password" />
				<br></br>
				<TextField
					helperText={confirmPasswordErrText}
					error={confirmPasswordErr}
					onChange={(e)=>{
						setConfirmPassword(e.target.value)
					}}
				id="filled-basic" label="Confirm Password" variant="filled" type="password" />

			<br></br>
			<div className = 'signupButtons'>
				<Button variant="outlined"
				onClick={()=>{
					navigate('/login')
				}}>or login</Button>

				<Button variant="contained"
				onClick={signupWithEmailAndPass}>Sign Up</Button>
			</div>

			<br></br>
			<Providers></Providers>
		</Box>
	</div>
	</>
	)
}

export default Register;
