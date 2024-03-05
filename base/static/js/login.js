  function loginUser(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        // Signed in
        var user = userCredential.user;
        // Redirect or show success
      })
      .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        // Show error message
      });
  }
