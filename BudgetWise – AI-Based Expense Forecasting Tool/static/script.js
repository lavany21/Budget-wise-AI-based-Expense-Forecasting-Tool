

function registerUser() {
    const email = document.querySelector('#register-box input[type="email"]').value;
    const password = document.getElementById("registerPassword").value;

    if (email === "" || password === "") {
        alert("Please enter email and password");
        return;
    }

    const storedUser = JSON.parse(localStorage.getItem("user"));

    // 🔥 If user already exists
    if (storedUser && storedUser.email === email) {
        alert("User already registered! Please login.");
        showLogin();
document.querySelector('#login-box input[type="email"]').value = email;
  // Switch to login form
        return;
    }

    // Save new user
    const user = {
        email: email,
        password: password
    };

    alert("Registration successful! Please login.");
    showLogin();
}


function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.type = input.type === "password" ? "text" : "password";
}
window.onload = function () {
    const params = new URLSearchParams(window.location.search);

    if (params.get("register") === "true") {
        showRegister();
    }
};
