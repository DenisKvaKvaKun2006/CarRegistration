document.addEventListener("DOMContentLoaded", async () => {
    const headerContainer = document.createElement("div");
    headerContainer.id = "header-container";
    document.body.prepend(headerContainer);

    try {
        const response = await fetch("/static/html/header.html");
        if (response.ok) {
            const headerHTML = await response.text();
            headerContainer.innerHTML = headerHTML;

            const loginButton = document.getElementById("login-button");
            const registerButton = document.getElementById("register-button");
            const logoutButton = document.getElementById("logout-button");

            const isLoggedIn = localStorage.getItem("token");

            if (isLoggedIn) {
                loginButton.style.display = "none";
                registerButton.style.display = "none";
                logoutButton.style.display = "block";

                logoutButton.addEventListener("click", () => {
                    localStorage.removeItem("token");
                    window.location.href = "/static/html/index.html";
                });
            } else {
                loginButton.style.display = "inline";
                registerButton.style.display = "inline";
                logoutButton.style.display = "none";
            }
        } else {
            console.error("Failed to load header.");
        }
    } catch (error) {
        console.error("Error loading header:", error);
    }
});
