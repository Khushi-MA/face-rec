// Utility: Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle signup form validation and submission
document.getElementById("signupForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const pass = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("signupConfirm").value;
    const error = document.getElementById("signupError");

    if (pass !== confirm) {
        error.textContent = "Passwords do not match.";
        error.classList.remove("d-none");
        return;
    }

    const data = {
        username: username,
        email: email,
        password: pass
    };

    fetch('/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
          if (data.error) {
              error.textContent = data.error;
              error.classList.remove("d-none");
          } else {
              alert("Signup successful!");
              error.classList.add("d-none");
              document.getElementById("signupForm").reset();
          }
      }).catch(err => {
          console.error(err);
          error.textContent = "An error occurred during signup.";
          error.classList.remove("d-none");
      });
});

// Handle login form validation and submission
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    const error = document.getElementById("loginError");

    if (!username || !password) {
        error.textContent = "Username and password are required.";
        error.classList.remove("d-none");
        return;
    }

    const data = { username, password };

    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => {
          if (data.error) {
              error.textContent = data.error;
              error.classList.remove("d-none");
          } else {
              alert("Login successful!");
              error.classList.add("d-none");
              document.getElementById("loginForm").reset();
              // You can redirect to dashboard or enable sleep form here
          }
      }).catch(err => {
          console.error(err);
          error.textContent = "An error occurred during login.";
          error.classList.remove("d-none");
      });
});

// Handle logout
document.getElementById("logoutBtn")?.addEventListener("click", function () {
    fetch('/logout/', {
        method: 'GET'
    }).then(response => response.json())
      .then(data => {
          alert("Logged out!");
          // Optionally redirect or hide protected UI
      }).catch(err => {
          console.error(err);
          alert("An error occurred while logging out.");
      });
});
