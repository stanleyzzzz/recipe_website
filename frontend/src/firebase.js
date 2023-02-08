import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD1z_nJPXdRFe3gryV1hZ4cHps7fTCCaLs",
  authDomain: "fantastic-recipes-dev.firebaseapp.com",
  projectId: "fantastic-recipes-dev",
  storageBucket: "fantastic-recipes-dev.appspot.com",
  messagingSenderId: "61361561437",
  appId: "1:61361561437:web:93af3476371e04fd3d52b4",
  measurementId: "G-4WYKWZS23D"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export default app;
