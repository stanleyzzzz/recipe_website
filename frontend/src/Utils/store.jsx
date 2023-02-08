import React, { useEffect, useState } from 'react';
import * as FirebaseAuth from 'firebase/auth';
import { auth } from '../firebase';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router';
import { postData } from '../Helpers/helpers.jsx';

export const StoreContext = React.createContext(null);

Store.propTypes = {
  children: PropTypes.object
}

// Store context
export default function Store({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [userError, setUserError] = useState("");

  const navigate = useNavigate();
	const googleProvider = new FirebaseAuth.GoogleAuthProvider();

  const register = (email, username, first_name, last_name, password) =>
    FirebaseAuth.createUserWithEmailAndPassword(auth, email, password)
      .then(userCredentials => {
        postData('http://localhost:8080/api/users', { firebase_id: userCredentials.user.uid, email, username, first_name, last_name })
      })
      .catch(err => {
        setUserError(err.message);
      });

  const login = (email, password) =>
    FirebaseAuth.signInWithEmailAndPassword(auth, email, password)


	const loginWithGoogle = () =>
		FirebaseAuth.signInWithPopup(auth, googleProvider)
      .then(userCredentials => {
        postData('http://localhost:8080/api/users', { firebase_id: userCredentials.user.uid, email: userCredentials.user.email, username: userCredentials.user.email, first_name: 'none', last_name: 'none' })
      })
      .catch(err => {
        setUserError(err.message);
      });


  const logout = () =>
    FirebaseAuth.signOut(auth)
      .catch(err => {
        setUserError(err.message);
      });

  const forgotPassword = (email) =>
    FirebaseAuth.sendPasswordResetEmail(auth)
      .catch(err => {
        setUserError(err.message);
      });

  useEffect(() => {
      const unsubscribe = FirebaseAuth.onAuthStateChanged(auth, user => {
        if (user)
          setCurrentUser({ email: user.email, id: user.uid });
        else
          setCurrentUser(null);
      });

      return unsubscribe;
  }, []);

  const store = {
    currentUser,
    userError,
    register,
    login,
		loginWithGoogle,
    logout,
    forgotPassword,
    navigate
  }

  return <StoreContext.Provider value={store}>
    {children}
  </StoreContext.Provider>
}
