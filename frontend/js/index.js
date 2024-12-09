// API base URL (Adjust this if the backend URL changes)
const apiUrl = "http://127.0.0.1:8000";

// Form handlers for adding a car and registration
document.getElementById("addCarForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const car = {
        make: document.getElementById("make").value,
        model: document.getElementById("model").value,
        license_plate: document.getElementById("license_plate").value
    };

    try {
        await fetch(`${apiUrl}/add_car/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(car)
        });
        fetchCars(); // Refresh the car list
    } catch (error) {
        console.error("Error adding car:", error);
    }
});

// Function to fetch and display cars
async function fetchCars() {
    try {
        const response = await fetch(`${apiUrl}/get_cars/`);
        const data = await response.json();

        const carList = document.getElementById("carList");
        carList.innerHTML = ""; // Clear the current list

        data.cars.forEach(car => {
            const li = document.createElement("li");
            li.innerHTML = `
                ${car.make} ${car.model} - ${car.license_plate}
                <button class="add-registration" onclick="showRegistrationForm('${car.license_plate}')">Add Registration</button>
                <button class="delete-car" onclick="deleteCar('${car.license_plate}')">Delete Car</button>
                <button class="delete-registration" onclick="deleteRegistration('${car.license_plate}')">Delete Registration</button>
            `;
            carList.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching cars:", error);
    }
}

// Show registration form for the selected car
function showRegistrationForm(licensePlate) {
    document.getElementById("reg_license_plate").value = licensePlate;
    document.getElementById("registrationFormSection").style.display = "block";
}

// Cancel registration form
document.getElementById("cancelRegistration").addEventListener("click", () => {
    document.getElementById("registrationFormSection").style.display = "none";
});

// Form handler for adding registration
document.getElementById("addRegistrationForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const registration = {
        license_plate: document.getElementById("reg_license_plate").value,
        owner_name: document.getElementById("owner_name").value,
        owner_address: document.getElementById("owner_address").value,
        year_of_manufacture: document.getElementById("year_of_manufacture").value
    };

    try {
        await fetch(`${apiUrl}/add_registration/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(registration)
        });
        fetchCars(); // Refresh the car list
        document.getElementById("registrationFormSection").style.display = "none"; // Hide the form after submitting
    } catch (error) {
        console.error("Error adding registration:", error);
    }
});

// Function to delete a car
async function deleteCar(licensePlate) {
    try {
        await fetch(`${apiUrl}/delete_car/${licensePlate}`, {
            method: "DELETE"
        });
        fetchCars(); // Refresh the car list
    } catch (error) {
        console.error("Error deleting car:", error);
    }
}

// Function to delete a registration
async function deleteRegistration(licensePlate) {
    try {
        await fetch(`${apiUrl}/delete_registration/${licensePlate}`, {
            method: "DELETE"
        });
        fetchCars(); // Refresh the car list
    } catch (error) {
        console.error("Error deleting registration:", error);
    }
}

// Initialize the car list on page load
fetchCars();
