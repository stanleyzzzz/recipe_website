import React, { useState } from 'react'
import ChatbotBubble from './ChatbotBubble'
import ChatbotModal from './ChatbotModal';

/*
	Modal and bubble for chatbot
	Page: Home
*/
function Chatbot() {
	const [showModal, setShowModal] = useState(false); // default state should be false
	let [messages, setMessages] = useState([{
		sender: "bot",
        message: "Hello! I'm fantastic bot, what can I help you with?", 
		type: "buttons"
	}])


	// opening the modal
	const openModal = () => {
		setShowModal(true);
	}

	// closing the modal
	const closeModal = () => {
		setShowModal(false);
	}


	if(showModal) {
		return <ChatbotModal messages={messages} setMessages={setMessages} closeModal={closeModal}/>;
	}

	return (
		<ChatbotBubble openModal={openModal} />
	)
}

export default Chatbot
