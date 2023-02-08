import { Box, Card } from '@mui/material';
import Navbar from '../../Components/Navbar';
import React, { useState } from 'react';
import { getData, updateData } from '../../Helpers/helpers.jsx';
import { StoreContext } from '../../Utils/store';
import AddIcon from '@mui/icons-material/Add';
import BlockIcon from '@mui/icons-material/Block';
import './styles.scss';

/*
	Admin dashboard that allows admin users to view all users and then unban or ban them
*/

function AdminDashboard() {
	const context = React.useContext(StoreContext);
	const { currentUser } = context;

  const [usersList, setUsersList] = useState([]);

  // fetch list of users using admin permission
	const fetchUsers = React.useCallback(() => {
    getData(`http://localhost:8080/api/users/list/${currentUser.id}`)
      .then(res => {
        return res.json();
      })
      .then(data => {
        setUsersList(data.users);
      })
      .catch(err => console.log(err));
	}, [currentUser.id])

  const toggleUserBan = (targetId, userIsBanned) => {
    if (userIsBanned) {
      updateData(`http://localhost:8080/api/users/unban/${targetId}`, {}, currentUser.id)
        .then(res => {
          fetchUsers();
        })
        .catch(err => {
          fetchUsers();
          console.error(err);
        })
    } else {
      updateData(`http://localhost:8080/api/users/ban/${targetId}`, {}, currentUser.id)
        .then(res => {
          fetchUsers();
        })
        .catch(err => {
          fetchUsers();
          console.error(err);
        })
    }
  }

	React.useEffect(() => {
    fetchUsers();
	}, [fetchUsers]);

	return (
    <>
      <Navbar />
      <div className="adminDashboardWrapper">
        <h1 className="shadowTxt">Admin Dashboard</h1>
          <Box className="usersBox">
            {!usersList.length && "No users"}
            <h2 className="shadowTxt" style={{"fontSize": "30px"}}>Ban users</h2>
            {usersList.map(user => (
              <Card key={user.user_id} className={"usersBoxCard " + (user.is_banned ? "isBanned" : "")}>
                <div>{user.username}</div>
                <div className="toggleIcon" onClick={() => toggleUserBan(user.user_id, user.is_banned)}>
                  {user.is_banned ? <AddIcon /> : <BlockIcon />}
                </div>
              </Card>
            ))}
          </Box>
      </div>
    </>
	)
}

export default AdminDashboard;
