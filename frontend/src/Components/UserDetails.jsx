import React, { useState } from 'react'
import PropTypes from 'prop-types'
import EditIcon from '@mui/icons-material/Edit';
import { useRef } from 'react';
import { Button } from '@mui/material';
import { updateData } from '../Helpers/helpers';
import { StoreContext } from '../Utils/store';
import { useEffect } from 'react';


function UserDetails({ details, email }) {

	// Context
	const context = React.useContext(StoreContext);
    const {  navigate, currentUser } = context;

	// References to inputs
	const fnInput = useRef(null);
	const lnInput = useRef(null);
	const uInput = useRef(null);
	
	// Details to upload 
	const [inputDetails, setInputDetails] = useState({
		'first': details.first_name,
		'last': details.last_name,
		'username': details.username
	}) 

	// Other variables required
	const [isError, setIsError] = useState(false);
	const [saveEnabled, setSaveEnabled] = useState(true);

	// Changes input 
	const changeInput = (inp, val, inputRef) => {

		setSaveEnabled(false); // when anything is changed, user can save changes
		if(val.length > 0) {
			setIsError(false);
			inputRef.current.classList.remove('errorInput');
		} else {
			setIsError(true);
		}
		
		inputDetails[inp] = val;
		setInputDetails({...inputDetails});
	}


	// Highlights the input as red
	const highlightInput = (inputRef) => {
		inputRef.current.classList.add('errorInput');
	}
	
	// Input errors 
	const inputError = (inputRef, err) => {
		highlightInput(inputRef);
		setIsError(true);
	}

	// Check for errors on inputs
	const checkInputs = () => {
		if(fnInput.current.value.length === 0) {
			inputError(fnInput);
		}

		if(uInput.current.value.length === 0) {
			inputError(uInput);
		}

		if(lnInput.current.value.length === 0) {
			inputError(lnInput);
		}
	}

	// Save changes of edits made to the profile
	const saveChanges = async() => {
		checkInputs();

		if(!isError) {

			let data = {
				username: uInput.current.value,
				first_name: fnInput.current.value,
				last_name: lnInput.current.value
			}
			console.log(JSON.stringify(data))
			const r = await updateData('http://127.0.0.1:8080/api/users/' + details.user_id, {
				"username": uInput.current.value,
				"first_name": fnInput.current.value,
				"last_name": lnInput.current.value
			});


			// only signed in users can access this page
			if(r) {
				alert("Changes saved!");
				navigate(0); // refresh
			}  else {
				alert("There are errors in your inputs!");
			}  
			            
		} else {
			setSaveEnabled(true);
			alert("There are errors in your inputs!");

		}
	}
	useEffect(() => {
		
	},[])

	return (
		<div>
				<p>First Name: 
				<input className="profileInput" 
				ref={fnInput}
				onChange={(e)=> {changeInput('first', e.target.value, fnInput)}}
				value={inputDetails['first']} ></input>
				<EditIcon className="editBtn" onClick={()=>{fnInput.current.focus()}}/> 
				</p>

				<p>Last Name: <input className="profileInput"
				ref={lnInput}

					onChange={(e)=> {changeInput('last', e.target.value, lnInput)}}
				value={inputDetails['last']} ></input>
				<EditIcon className="editBtn" onClick={()=>{lnInput.current.focus()}} /></p>

				<p>Username: <input className="profileInput"
				ref={uInput}
				onChange={(e)=> {changeInput('username', e.target.value, uInput)}}
				value={inputDetails['username']} ></input>
				<EditIcon className="editBtn" onClick={()=>{uInput.current.focus()}}/></p>
				<p>Email: {email}</p>

				<Button className='saveBtn' 
				onClick={()=>{saveChanges()}}
				disabled = {saveEnabled}
				 variant='outlined' 
				 color='success'>Save changes</Button>
			 
		</div>
	)
}


export default UserDetails;
