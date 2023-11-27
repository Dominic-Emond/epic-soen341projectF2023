/*Purpose of this section: HTML => JSON
 *Obtaining information from the HTML forms in the form of a JavaScript Object and transforming it into JSON format
 */ 

 //Code for CREATE ACCOUNT
 document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.getElementById("registrationForm");
    const createAccountButton = document.getElementById("createAccountButton");

    createAccountButton.addEventListener("click", function (e) {
        e.preventDefault();

        const fullName = document.getElementById("fullName").value;
        const email = document.getElementById("email").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const isBroker = document.getElementById("broker").value;
        const isClient = document.getElementById("client").value;

        /* Capture the account type*/ 
        var type = isBroker ? "broker" : "client";
        // Create a JavaScript object to represent the user data
        const userData = {
            First_Name: fullName.split(' ')[0],
            Last_Name: fullName.split(' ')[1] || '',
            Email_Address: email,
            Username: username,
            Pass: password
        };

        // Convert the JavaScript object to a JSON string
        const jsonData = JSON.stringify(userData);

        // Simulate sending the JSON data to the backend API
        console.log("JSON Data to Send to Backend:", jsonData);
         // Make an HTTP POST request to your local API
         fetch(`http://127.0.0.1:8000/${type}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: jsonData,
        })
        .then((response) => {
            if (response.ok) {
                // Handle a successful response (e.g., show a success message)
                alert("Account created successfully!");
                window.location.replace("PropertyListing.html");
            } else {
                // Handle errors (e.g., display an error message)
                alert("Failed to create an account. Please try again.");
            }
        })
        .catch((error) => {
            // Handle network or other errors
            alert("An error occurred. Please try again later.");
            console.error(error);
        });
    });
});

//Code for Sign In
document.addEventListener("DOMContentLoaded", function () {
    const registrationForm = document.getElementById("logInForm");
    const createAccountButton = document.getElementById("signInButton");

    createAccountButton.addEventListener("click", function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        // Create a JavaScript object to represent the user data
        const signInData= {
            username,
            password,
        };

        // Convert the JavaScript object to a JSON string
        const jsonData = JSON.stringify(signInData);

        // Simulate sending the JSON data to the backend API
        console.log("JSON Data to Send to Backend:", jsonData);

         // Make an HTTP POST request to your local API
         fetch("http://localhost:8000/api/create-account", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: jsonData,
        })
        .then((response) => {
            if (response.ok) {
                // Handle a successful response (e.g., show a success message)
                alert("Account created successfully!");
            } else {
                // Handle errors (e.g., display an error message)
                alert("Failed to create an account. Please try again.");
            }
        })
        .catch((error) => {
            // Handle network or other errors
            alert("An error occurred. Please try again later.");
            console.error(error);
        });
    });
});