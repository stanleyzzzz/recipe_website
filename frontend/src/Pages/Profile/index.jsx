import React, { useState } from 'react';
import Navbar from '../../Components/Navbar';
import UserDetails from '../../Components/UserDetails';
import { StoreContext } from '../../Utils/store';
import { getData } from '../../Helpers/helpers';
import ProfilePicBtn from '../../Components/ProfilePicBtn';
import { Box, Button, CircularProgress, touchRippleClasses } from '@mui/material';
import './styles.scss'
import { purple, red } from '@mui/material/colors';


// Profile Settings for a single user
function Profile() {
    let [details, setDetails] = useState('');
    let [loading, setLoading] = useState(true);

    const context = React.useContext(StoreContext);
	const { navigate, currentUser} = context;

    // Gets data of signed in user
    React.useEffect(() => {

        // fetch using helper functions
        const getUserDetails = async() => {
            if(currentUser) {
                //console.log(currentUser)
                const resUser = await getData('http://127.0.0.1:8080/api/users/' + currentUser.id);  // TODO replace this
                const dataUser = await resUser.json();

                // only signed in users can access this page
                if(dataUser) {
                    setDetails(dataUser);
                    setLoading(false);
                }  else {
                    navigate("/");
                }
            }
        }

       getUserDetails();

       //console.log(currentUser, details)
    }, [currentUser])


    if(loading) {
        return <><Navbar/> <CircularProgress /></>
    } else {
    return (
        <>
            <Navbar/>

            <div className="profileSettingsWrapper">
                <h1 className="shadowTxt">Profile Settings</h1>
                <div className="generalInformation">

                    <ProfilePicBtn size="medium"/>
                    <p className = 'boldTxt'> Welcome back, {details.first_name} {details.last_name}!</p>
                    <p className = 'lightTxt'> Manage your info and recipes to make our site work better for you.</p>
                </div>

                <Box className="detailsBox">
                    {currentUser !== '' &&
                    <UserDetails details={details} email={currentUser.email}/>
                    }

                    <div className='profileBtns'>

                        <Button
                        onClick={()=>{
                            navigate('/profile/recipes/');
                        }}
                        color='success' variant="contained">View my recipes</Button>
                        {details.is_admin &&
                        <Button
                        onClick={()=>{
                                navigate('/admin/dashboard');
                        }}
                        className='dashboardBtn'
                        color='info'
                        variant='contained'>Admin Dashboard</Button>
                        }
                    </div>
                </Box>



            </div>
        </>

    )
                    }
}

export default Profile;
