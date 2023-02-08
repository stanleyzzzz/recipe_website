import { Box, Button, TextField, Typography } from '@mui/material'
import React, { useRef } from 'react'
import CloseIcon from '@mui/icons-material/Close';
import { useEffect } from 'react';
import { getData, postData } from '../Helpers/helpers';
import { useState } from 'react';
import { StoreContext } from '../Utils/store';


/* 
	Modal for chatbot
	Page: Home
*/
function ChatbotModal({closeModal, messages, setMessages}) {

	// For scrolling messages
	const messagesRef = useRef(null);
	const textRef = useRef(null);
	const context = React.useContext(StoreContext);
	
	// Variables for searching, asking a question and disabling chat
	let [chatDisabled, setChatDisabled] = useState(false);
	let [isSearchEnabled, setIsSearchEnabled] = useState(false);
	let [isRecommendEnabled, setIsRecommendEnabled] = useState(false);
	const [text, setText] = useState('');


	// Bot reply, takes in reply message, the type of message it is
	// and if there are recipe links
	const botReply = async(reply, type, recipeLinks) => {
		// Timeouts so message replies aren't jarring
		setTimeout(() => {
			setMessages([...messages, {
				sender: "bot",
				message: reply,
				type: type, 
				recipeLinks: recipeLinks
			}])
		}, 500);

		setTimeout(() => {
			messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
		},600)
	}

	// For when user sends a message
	const userReply = async(reply, type) => {
		messages.push({
			sender: "user",
			message: reply, 
			type: "none"
		});
		setMessages([...messages])
		setTimeout(() => {
			messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
		},1)
	}

	// Returns and replies with popular recipes
	const popularReply = async() => {
		const res =  await getData("http://127.0.0.1:8080/api/recipes?sort=ratings");
		const recipes = await res.json();
		let arr = recipes.slice(0, 5);
		if(recipes.length > 0) {
			botReply("Here's the most popular recipes: ", "links", arr);
		} else {
			botReply("No recipes currently exist on the website...");
		}
		setIsSearchEnabled(false);
	}

	// Uses whatever the user searches to search db for recipe
	const searchReply = async(msg) => {
		const res =  await getData("http://127.0.0.1:8080/api/recipes?name="+msg);
		const recipes = await res.json();
		if(recipes.length > 0) {
			botReply("Here's the recipes I found: ", "links", recipes);
		}
		else {
			botReply("No recipes with the name " + msg, "none");
		}

		// disables the search
		setIsSearchEnabled(false);
		setIsRecommendEnabled(false);
	}

	// Recommends user recipes based on ingredients they input
	const recommendReply = async(msg) => {
		const res =  await getData("http://127.0.0.1:8080/api/recipes?whitelist="+msg);
		const recipes = await res.json();
		if(recipes.length > 0) {
			botReply("Here's the recipes I recommend: ", "links", recipes);
		}
		else {
			botReply("No recipes with those ingredients!");
		}

		// disables the recommendation
		setIsSearchEnabled(false);
		setIsRecommendEnabled(false);
	}

	// Chooses the bot reply based on the message
	const chooseReply = (msg) => {
		let lcMsg = msg.toLowerCase(); // lowercase so it's not case sensitive

		if(lcMsg.includes("search")) {
			// For searching recipes
			botReply("Please give me a keyword to search:", "none");
			setIsSearchEnabled(true);
			return;
		} else if(lcMsg.includes("popular")) {
			// For giving the most popular recipes based on ratings
			popularReply();
			return;
		} else if(lcMsg.includes("suggest")) {
			// For suggesting recipes based on ingredients
			botReply("Enter some ingredients separated by commas:", "none")
			setIsRecommendEnabled(true);
			return;
		} else if(lcMsg.includes("hello") ||  lcMsg.includes("hey") || lcMsg.includes("hi")) {
			// Say hello!
			botReply("Hey there, I'm Fantastic Bot 😀 Ask me a question!", "none")
			return;
		} else if(lcMsg.includes("thank")) {
			// Thanks fantastic bot!
			botReply("My pleasure 😁 Any other questions?", "none")
			return;
		}
		else if(lcMsg.includes("no")) {
			// No!
			botReply("All good! Feel free to search our website for more recipes!", "none")
			return;
		}
		else {
			// Generic reply
			botReply("I don't understand " + msg.toLowerCase() + "..." + " Try one of these buttons!", "buttons");
		}		
	}


	// Send a message and return a reply
	const sendMsg = async(msg) => {
		// User reply
		userReply(msg, "none");
		
		// Bot Reply
		if(!isSearchEnabled && !isRecommendEnabled) {
			chooseReply(msg);
		} else if(isSearchEnabled) {
			searchReply(msg);
		} else if(isRecommendEnabled) {
			recommendReply(msg);
		}

		// Disable the chat briefly
		setTimeout(() => {
			messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
			setChatDisabled(false);
		}, 600);	
	}
	
	// Each message has different functionality
	// Links contains links of recipes
	// buttons contains buttons to press
	// none are for generic replies
	return (
		<Box className="chatbotModal">
			<Box className="chatbotModalBar">
				<Box className="chatbotTitleWrapper">
					<Typography>Fantastic Bot</Typography>
				</Box>
				<CloseIcon 
				className="closeChatbotModalBtn"
				color="error"
				sx={{
					cursor:"pointer",
				}} 
				onClick={ closeModal }/>
			</Box>

			<Box ref = {messagesRef} className="chatbotMsgArea">
				{messages.map((msg) => {
					if(msg.type === "none") {
						return (
							<Box
							className={"msg " + msg.sender + "Msg"}
							>
								<b>{msg.sender.toUpperCase()}:</b> {msg.message}
							</Box>
						)
					} else if(msg.type === "links") {
						return (
							<Box
							className={"msg " + msg.sender + "Msg"}
							>
								<b>{msg.sender.toUpperCase()}:</b> {msg.message}<br/>
								
							
								{msg.recipeLinks.map((l, n) => 
								{
									return <p>
										{n+1}. <a onClick={()=>{window.open("http://localhost:3000/recipe/" + l.recipe_id, '_blank');}}>{l.title}</a></p>
								})}
		
							</Box>
						)
					}
					
					else {
						return (
							<Box
							className={"msg " + msg.sender + "Msg"}
							>
								<b>{msg.sender.toUpperCase()}:</b> {msg.message}<br/>
								<div className="chatbotBtns">
								<Button className="chatbotBtn" variant="contained"
								onClick={()=>{
									setIsSearchEnabled(false);
									setIsRecommendEnabled(false);
									botReply("Please give me a keyword to search:", "none")
									setIsSearchEnabled(true);
								}}>1. Keyword Recipe Search</Button><br/>

								
								<Button className="chatbotBtn" variant="contained"
								onClick={()=>{
									setIsSearchEnabled(false);
									setIsRecommendEnabled(false);
									botReply("Enter some ingredients separated by commas", "none")
									setIsRecommendEnabled(true);
								}}
								>2. Recipe Suggestion</Button><br/>
								<Button className="chatbotBtn" variant="contained"
								onClick={()=>{
									//userReply("Give me some recipes.")
									popularReply();
								}}
								>3. Popular Recipes</Button><br/>
								</div>
							</Box>
						)
					}
				})}
			

			</Box>
			<input 
			disabled={chatDisabled}
			onKeyDown={(e)=> {
				setText(e.target.value);	
			}}
			onKeyUp={(e) => {
				if(e.key === "Enter") {
					sendMsg(text);
					setText('');
					textRef.current.value = '';
					setChatDisabled(true);
				}
			}}
			ref={textRef}
			placeholder="Ask a question" className="chatbotInput"/>

		</Box>
	)
}

export default ChatbotModal
