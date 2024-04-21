// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object

// TODO: SAFELY STORE IN ENVIRONMENT VARIABLES AND CALL FROM THE BACKEND
const firebaseConfig = {
    apiKey: "AIzaSyC7FAzJTsq4pzYPSK1INMzYSGNtk74G8AI",
    authDomain: "srslingo.firebaseapp.com",
    projectId: "srslingo",
    storageBucket: "srslingo.appspot.com",
    messagingSenderId: "234027864352",
    appId: "1:234027864352:web:5b8673dffcb199898c4745",
    measurementId: "G-GY002C3EZ7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

// Sign in with Google
const googleSignIn = () => {
  const provider = new GoogleAuthProvider();
  signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access Google APIs.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      // The signed-in user info.
      const user = result.user;
      // You can redirect the user to another page or update the UI accordingly
      console.log("User signed in:", user);
    }).catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
      console.error("Error during sign in:", errorMessage);
    });
};

// Sign out
const googleSignOut = () => {
  signOut(auth).then(() => {
    // Sign-out successful.
    console.log("User signed out.");
  }).catch((error) => {
    // An error happened.
    console.error("Error signing out:", error);
  });
};

// Function to login using Email and Password
function loginUser(email, password) {
  const auth = firebase.auth();
  auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Get ID token
      userCredential.user.getIdToken().then(idToken => {
        // Send token to Django backend
        fetch('/verify-token/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({ token: idToken }),
        })
        .then(response => response.json())
        .then(data => {
          // Handle response
          if(data.success) {
            window.location.href = '/dashboard'; // Or wherever you wish to redirect
          }
        });
      });
    })
    .catch((error) => {
      alert(error.message); // Simplistic error handling
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Attach sign-in event listener
    const loginButton = document.getElementById('google-login');
    const registerButton = document.getElementById('google-register');

    if (loginButton) {
        loginButton.addEventListener('click', googleSignIn);
    }

    if (registerButton) {
        registerButton.addEventListener('click', googleSignIn);
    }

    // Optional: Attach sign-out event listener
    const signOutButton = document.getElementById('google-signout'); // Ensure you have a button with this ID for sign-out
    if (signOutButton) {
        signOutButton.addEventListener('click', googleSignOut);
    }
});

firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
    // Send token to your backend via HTTPS
    fetch('/verify-token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Ensure you're getting the CSRF token correctly
        },
        body: JSON.stringify({token: idToken})
    }).then(response => response.json())
    .then(data => {
        console.log(data); // Handle response data
    });
}).catch(function(error) {
    // Handle error
});

// Listening for auth state changes for sign in and sign out
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in, you can get the signed in user's information
    console.log("User is signed in:", user);
  } else {
    // User is signed out
    console.log("User is signed out.");
  }
});


// Exporting functions if you want to use them in specific scripts or HTML pages
export { googleSignIn, googleSignOut };