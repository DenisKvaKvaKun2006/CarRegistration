const regList = document.getElementById("regList");
const addRegButton = document.getElementById("addRegButton");
const addRegForm = document.getElementById("addRegForm");
const submitAddReg = document.getElementById("submitAddReg");
const searchRegInput = document.getElementById("searchRegInput");
const searchRegButton = document.getElementById("searchRegButton");

const API_BASE = "/regdb";


const AUTH_TOKEN = localStorage.getItem("token");


if (!AUTH_TOKEN) {
    alert("Вы не авторизованы. Перейдите на страницу входа.");
    window.location.href = "/static/html/login.html";
}


async function authorizedFetch(url, options = {}) {
    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${AUTH_TOKEN}`,
        "Content-Type": "application/json"
    };

    const response = await fetch(url, options);


    if (response.status === 401) {
        alert("Сессия истекла. Пожалуйста, войдите снова.");
        window.location.href = "/static/html/login.html";
        return null;
    }


    if (!response.ok) {
        const errorData = await response.json();
        console.error("Ошибка запроса:", errorData.detail);
        alert(`Ошибка: ${errorData.detail}`);
        return null;
    }

    return response;
}


async function loadRegs() {
    const response = await authorizedFetch(`${API_BASE}/get_registrations/`);

    if (!response || !response.ok) {
        console.error("Ошибка загрузки регистраций:", response?.statusText);
        return;
    }

    const data = await response.json();

    if (data && Array.isArray(data.registrations)) {
        const regs = data.registrations;

        if (regs.length === 0) {
            regList.innerHTML = "<li>Нет доступных регистраций</li>";
        } else {
            regList.innerHTML = "";
            regs.forEach(reg => {
                const li = document.createElement("li");
                li.setAttribute("data-license_plate", reg.license_plate);
                li.setAttribute("data-owner_name", reg.owner_name);
                li.setAttribute("data-owner_address", reg.owner_address);
                li.setAttribute("data-year", reg.year_of_manufacture);
                li.innerHTML = `
                    <strong>${reg.license_plate}</strong>
                    <button class="expand">Данные</button>
                    <button class="green">Найти автомобиль</button>
                    <button class="delete">Удалить</button>
                    <div class="reg-details hidden">
                        <p>Номер: <strong>${reg.license_plate}</strong></p>
                        <p>Владелец: <strong>${reg.owner_name}</strong></p>
                        <p>Адрес владельца: <strong>${reg.owner_address}</strong></p>
                        <p>Год выпуска: <strong>${reg.year_of_manufacture}</strong></p>
                    </div>
                `;
                regList.appendChild(li);


                li.querySelector(".expand").addEventListener("click", () => {
                    const details = li.querySelector(".reg-details");
                    details.classList.toggle("hidden");
                });


                li.querySelector(".green").addEventListener("click", async () => {
                    const licensePlate = reg.license_plate;
                    const carResponse = await authorizedFetch(`/carsdb/get_cars/`);
                    const cars = await carResponse.json();
                    const car = cars.find(c => c.license_plate === licensePlate);

                    if (car) {
                        window.location.href = `/carsdb/get_cars.html?license_plate=${car.license_plate}`;
                    } else {
                        alert("Автомобиль с таким номером не найден.");
                    }
                });


                li.querySelector(".delete").addEventListener("click", async () => {
                    if (confirm("Удалить регистрацию?")) {
                        const deleteResponse = await authorizedFetch(`${API_BASE}/delete_registration/${reg.license_plate}`, {
                            method: "DELETE"
                        });
                        if (deleteResponse && deleteResponse.ok) {
                            loadRegs();
                        }
                    }
                });
            });
        }
    } else {
        console.error("Ответ сервера не содержит корректный список регистраций:", data);
        alert("Ошибка загрузки регистраций.");
    }
}

addRegButton.addEventListener("click", () => {
    addRegForm.classList.toggle("hidden");
});

submitAddReg.addEventListener("click", async () => {
    const licensePlate = document.getElementById("newRegLicensePlate").value;
    const ownerName = document.getElementById("newOwnerName").value;
    const ownerAddress = document.getElementById("newOwnerAddress").value;
    const yearOfManufacture = document.getElementById("newYearOfManufacture").value;

    if (licensePlate && ownerName && ownerAddress && yearOfManufacture) {
        const response = await authorizedFetch(`${API_BASE}/add_registration/`, {
            method: "POST",
            body: JSON.stringify({
                license_plate: licensePlate,
                owner_name: ownerName,
                owner_address: ownerAddress,
                year_of_manufacture: parseInt(yearOfManufacture)
            })
        });

        if (response) {
            addRegForm.classList.add("hidden");
            loadRegs();
        } else {
            alert("Ошибка добавления регистрации.");
        }
    } else {
        alert("Введите все данные о регистрации.");
    }
});

searchRegButton.addEventListener("click", () => {
    const query = searchRegInput.value.toLowerCase();
    const regs = document.querySelectorAll("li");
    let found = false;

    const noResultsMessage = document.querySelector(".no-results");
    if (noResultsMessage) {
        noResultsMessage.remove();
    }
    regs.forEach(reg => {
        const licensePlate = reg.getAttribute("data-license") || "";
        const OwnerName = reg.getAttribute("data-owner_name") || "";
        const OwnerAddress = reg.getAttribute("data-owner_address") || "";
        const Year = reg.getAttribute("data-year") || "";

        if (licensePlate.toLowerCase().includes(query) || OwnerName.toLowerCase().includes(query) || OwnerAddress.toLowerCase().includes(query) || Year.toLowerCase().includes(query)) {
            reg.style.display = "";
            found = true;
        } else {
            reg.style.display = "none";
        }
    });

    if (!found && query !== "") {
        if (!document.querySelector(".no-results")) {
            const noResultsMessage = document.createElement("li");
            noResultsMessage.classList.add("no-results");
            noResultsMessage.textContent = "Регистрации не найдены.";
            regList.appendChild(noResultsMessage);
        }
    }
});

loadRegs();
