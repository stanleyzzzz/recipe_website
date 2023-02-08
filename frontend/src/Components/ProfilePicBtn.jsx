import { Button } from '@mui/material'
import React from 'react'
import { StoreContext } from '../Utils/store';

const smallBtn ={
    borderRadius: '50%',
    padding: '0',
    minWidth: '0px',
    width: '40px',
    height: '40px',
    fontSize: '20px',
    background: '',
    fontWeight: '900'
}

const mediumBtn ={
    borderRadius: '50%',
    padding: '0',
    width: '50px',
    height: '60px',
    fontSize: '30px',
    background: '',
    fontWeight: '900'
}

const profileBtns = {
    'small': smallBtn,
    'medium': mediumBtn,
}

function ProfilePicBtn({ size, sx }) {
    const context = React.useContext(StoreContext);
    const { currentUser, navigate } = context;
    if(!size) {
        size = "small";
    }

    if(!currentUser) {
        return (      <Button
            color="info"
            variant="contained"
            sx={profileBtns[size]}
            onClick={()=>{navigate('/profile')}}>
            ?</Button>)
    }
    return (
        <Button
        color="info"
        variant="contained"
        sx={profileBtns[size]}
        onClick={()=>{navigate('/profile')}}>
        {currentUser.email[0]}</Button>
    )

}

export default ProfilePicBtn
