// Toggle the form between login and register
function toggleForm(formType) {
  const loginBox = document.querySelector('.login-box');
  const registerBox = document.querySelector('.register-box');

  if (formType === 'login') {
    loginBox.classList.add('show');
    registerBox.classList.remove('show');
  } else {
    registerBox.classList.add('show');
    loginBox.classList.remove('show');
  }
}

// Toggle password visibility
function togglePasswordVisibility(id) {
  const passwordField = document.getElementById(id);
  const type = passwordField.type === 'password' ? 'text' : 'password';
  passwordField.type = type;
}

// Password and Confirm Password Validation
document.getElementById("register-form").addEventListener("submit", function (e) {
  const password = document.getElementById("register-password").value;
  const confirmPassword = document.getElementById("register-confirm-password").value;
  const passwordError = document.getElementById("password-error");

  if (password !== confirmPassword) {
    e.preventDefault();
    passwordError.style.display = "block";
  } else {
    passwordError.style.display = "none";
  }
});

// Registration Form Submission
document.getElementById("register-form").addEventListener("submit", function(e) {
  e.preventDefault();
  
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;
  const confirmPassword = document.getElementById("register-confirm-password").value;
  
  fetch('/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&confirm_password=${encodeURIComponent(confirmPassword)}`
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === "error") {
          alert(data.message);
      } else if (data.status === "success") {
          alert(data.message);
          window.location.href = '/';  // Redirect to homepage or login page
      }
  })
  .catch(error => console.error('Error:', error));
});

// Login Form Submission
document.getElementById("login-form").addEventListener("submit", function(e) {
  e.preventDefault();  // Prevent default form submission
  
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === "error") {
          alert(data.message);
      } else if (data.status === "success") {
          window.location.href = '/success';  // Redirect to success page
      }
  })
  .catch(error => console.error('Error:', error));
});