import { Button } from '@mui/material'
import React from 'react'
import ChatBubbleIcon from '@mui/icons-material/ChatBubble';


/* 
    Bubble for chatbot 
    Page: Home
*/

const mediumBtn ={
    borderRadius: '50%',
    padding: '0',
    width: '50px',
    height: '60px',
    fontSize: '30px',
    background: '',
    fontWeight: '900',
    position: 'fixed',
    top: '90%',
    left: '93%',
    background: '#01579b'
}


function ChatbotBubble({ openModal }) {
    return (
        <Button
        sx={mediumBtn}

        variant="contained"
        onClick={ openModal }>
            <ChatBubbleIcon/>
        </Button>
    )
}

export default ChatbotBubble
