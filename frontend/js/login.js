document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("token", data.access_token);
            alert("Login successful!");
            window.location.href = "/static/html/index.html";
        } else {
            const data = await response.json();
            alert(data.detail || "Login failed.");
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    }
});
