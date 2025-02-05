import { apiRequest } from "./Handshake.js";

document.getElementById('toggle-form').addEventListener('click', function(event) {
    event.preventDefault();
    const formTitle = document.getElementById('form-title');
    const authButton = document.getElementById('auth-button');
    const extraFields = document.getElementById('extra-fields');
    
    if (formTitle.innerText === 'Sign In') {
        formTitle.innerText = 'Sign Up';
        authButton.innerText = 'Sign Up';
        extraFields.style.display = 'block';
        this.innerText = 'Already have an account? Sign In';
    } else {
        formTitle.innerText = 'Sign In';
        authButton.innerText = 'Sign In';
        extraFields.style.display = 'none';
        this.innerText = "Don't have an account? Sign Up";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Populate email field from local storage
    const savedEmail = localStorage.getItem('email');
    if (savedEmail) {
        document.getElementById('email').value = savedEmail;
    }
});

document.getElementById('verify-code').addEventListener('input', function() {
    if (this.value.length === 6) {
        const formData = new FormData(document.getElementById('verify-form'));
        const jsonObject = Object.fromEntries(formData.entries());
        apiRequest("/validate_email_code", "POST", jsonObject)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }

                if (res.status === 204) {
                    // Effectively we need to clear out the sign-in/sign-up stuff and replace it with the account stuff
                }
            })
            .catch(error => console.error('Error:', error));   
    }
});

document.getElementById('auth-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const isSignUp = document.getElementById('form-title').innerText === 'Sign Up';
    const jsonObject = Object.fromEntries(formData.entries());

    // Save email to local storage
    localStorage.setItem('email', jsonObject['email']);

    if (isSignUp && jsonObject['password'] !== jsonObject['confirm-password']) {
        delete jsonObject['confirm-password'];
        alert('Passwords do not match');
        return;
    }

    if (isSignUp) {
        apiRequest("/register_user", "POST", jsonObject)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                if (res.status === 204) {
                    document.getElementById('verify-form').style.display = 'block';
                    document.getElementById('auth-form').style.display = 'none';
                    return;
                }
            })
            .catch(error => console.error('Error:', error));
        return; // Ensure the sign-in request is not sent if registration is attempted
    }
    apiRequest("/sign_user_in", "POST", jsonObject)
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

});