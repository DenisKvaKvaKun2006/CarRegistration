document.getElementById("registration-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Сбор данных с формы
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
                confirm_password: confirmPassword,
            }),
        });

        if (response.ok) {
            alert("Registration successful! Please login.");
            window.location.href = "login.html"; // Перенаправление на страницу логина
        } else {
            const data = await response.json();
            alert(data.detail || "Registration failed.");
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    }
});
