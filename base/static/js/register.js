  function registerUser(email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
        // Signed in
        var user = userCredential.user;
        // You can redirect the user to another page or show a success message
      })
      .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        // Show an error message to the user.
      });
  }
