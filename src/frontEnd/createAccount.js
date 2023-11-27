// Function to create an account
async function createAccount(accountType) {
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const url = `http://127.0.0.1:8000/${accountType}s`; // Assuming the endpoint follows the pattern /clients or /brokers

    const accountData = {
        First_Name: fullName.split(' ')[0],
        Last_Name: fullName.split(' ')[1] || '',
        Email_Address: email,
        Username: username,
        Pass: password
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(accountData),
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result);

            // Show success message
            document.getElementById('successMessage').style.display = 'block';

            
        } else {
            // If the response status is not ok, handle the error
            console.error('Account creation failed:', response.statusText);
        }
    } catch (error) {
        console.error('Error during account creation:', error);
    }
}

// Event listeners for the buttons
document.getElementById('createAccountButton').addEventListener('click', function () {
    const accountType = document.querySelector('input[name="accountType"]:checked').value;

    if (!accountType) {
        alert('Please select an account type (broker or client).');
        return;
    }

    createAccount(accountType);
});
