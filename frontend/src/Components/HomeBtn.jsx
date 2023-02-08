import { Button } from '@mui/material';
import React from 'react'
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { StoreContext } from '../Utils/store';

function HomeBtn() {
    const context = React.useContext(StoreContext);

    const { navigate } = context;

    return (
        <Button onClick={()=>{
            navigate('/')
        }}>
            <ArrowBackIcon></ArrowBackIcon>
            Return Home
        </Button>
    )
}

export default HomeBtn
