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
const licensePlateRegex = /^[A-Z]{1}\d{3}[A-Z]{2}\d{2,3}$/;
const ownerNameRegex = /^[a-zA-Zа-яА-ЯёЁ\s\-]{1,50}$/;
const ownerAddressRegex = /^[А-Яа-яЁёA-Za-z0-9\s.,-\\/]+$/;
const yearRegex = /^(19|20)\d{2}$/;

const urlParams = new URLSearchParams(window.location.search);
const licensePlateFromURL = urlParams.get("license_plate");

if (licensePlateFromURL) {
    const licensePlateInput = document.getElementById("newRegLicensePlate");

    if (licensePlateInput) {
        licensePlateInput.value = licensePlateFromURL;
        licensePlateInput.setAttribute("readonly", "readonly");

        const addRegForm = document.getElementById("addRegForm");
        if (addRegForm) {
            addRegForm.classList.remove("hidden");
        }
    } else {
        console.error("Field with ID 'newRegLicensePlate' not found in the HTML!");
    }
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
                    <div class="button-row">
                        <button class="expand">Данные</button>
                        <button class="edit-reg">Редактировать</button>
                        <button class="find-car">Найти автомобиль</button>
                        <button class="delete">Удалить</button>
                    </div>
                    <div class="reg-details hidden">
                        <p>Номер: <strong>${reg.license_plate}</strong></p>
                        <p>Владелец: <strong>${reg.owner_name}</strong></p>
                        <p>Адрес владельца: <strong>${reg.owner_address}</strong></p>
                        <p>Год выпуска: <strong>${reg.year_of_manufacture}</strong></p>
                    </div>
                    <div class="car-result hidden">
                        <p class="car-info"></p>
                        <button class="hide-car-result hidden">Скрыть</button>
                    </div>
                `;
                regList.appendChild(li);

                li.querySelector(".edit-reg").addEventListener("click", () => showEditRegForm(reg));

                li.querySelector(".find-car").addEventListener("click", async () => {
                    const licensePlate = reg.license_plate;
                    const carResultDiv = li.querySelector(".car-result");
                    const carInfoParagraph = carResultDiv.querySelector(".car-info");
                    const hideCarResultButton = carResultDiv.querySelector(".hide-car-result");

                    carInfoParagraph.textContent = "Загрузка...";
                    hideCarResultButton.classList.add("hidden");

                    const carResponse = await authorizedFetch(`/carsdb/search_cars/?query=${licensePlate}`);

                    carInfoParagraph.textContent = "";

                    if (carResponse) {
                        const data = await carResponse.json();
                        const car = data.cars.find(c => c.license_plate === licensePlate);

                        if (car) {
                            carInfoParagraph.innerHTML = `
                                <strong>Данные автомобиля:</strong><br>
                                Марка: ${car.make}<br>
                                Модель: ${car.model}<br>
                                Номер: ${car.license_plate}
                            `;
                        } else {
                            carInfoParagraph.textContent = "Автомобиль с таким номером не найден.";
                        }
                    } else {
                        carInfoParagraph.textContent = "Ошибка при загрузке данных об автомобиле.";
                    }

                    carResultDiv.classList.remove("hidden");

                    hideCarResultButton.classList.remove("hidden");
                    hideCarResultButton.addEventListener("click", () => {
                        carResultDiv.classList.add("hidden");
                    });
                });

                li.querySelector(".expand").addEventListener("click", () => {
                    const details = li.querySelector(".reg-details");
                    details.classList.toggle("hidden");
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

submitAddReg.addEventListener("click", async () => {
    const licensePlateInput = document.getElementById("newRegLicensePlate");
    const ownerNameInput = document.getElementById("newOwnerName");
    const ownerAddressInput = document.getElementById("newOwnerAddress");
    const yearInput = document.getElementById("newYearOfManufacture");

    const licensePlate = licensePlateInput.value.trim();
    const ownerName = ownerNameInput.value.trim();
    const ownerAddress = ownerAddressInput.value.trim();
    const year = yearInput.value.trim();

    const isLicensePlateValid = licensePlateRegex.test(licensePlate);
    const isOwnerNameValid = ownerNameRegex.test(ownerName);
    const isOwnerAddressValid = ownerAddressRegex.test(ownerAddress);
    const isYearValid = yearRegex.test(year) && year >= 1900 && year <= new Date().getFullYear();

    setFieldValidationStyle(licensePlateInput, isLicensePlateValid);
    setFieldValidationStyle(ownerNameInput, isOwnerNameValid);
    setFieldValidationStyle(ownerAddressInput, isOwnerAddressValid);
    setFieldValidationStyle(yearInput, isYearValid);

    if (!isLicensePlateValid || !isOwnerNameValid || !isOwnerAddressValid || !isYearValid) {
        alert("Пожалуйста, исправьте ошибки в форме перед добавлением регистрации.");
        return;
    }

    const response = await authorizedFetch(`${API_BASE}/add_registration/`, {
        method: "POST",
        body: JSON.stringify({
            license_plate: licensePlate,
            owner_name: ownerName,
            owner_address: ownerAddress,
            year_of_manufacture: parseInt(year, 10),
        }),
    });

    if (response) {
        addRegForm.classList.add("hidden");
        loadRegs();
    } else {
        alert("Ошибка добавления регистрации.");
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

function setFieldValidationStyle(input, isValid) {
    if (isValid) {
        input.style.border = "2px solid green";
    } else {
        input.style.border = "2px solid red";
    }
}

function showEditRegForm(reg) {
    const editRegForm = document.getElementById("editRegForm");
    const editRegLicensePlate = document.getElementById("editRegLicensePlate");
    const editOwnerName = document.getElementById("editOwnerName");
    const editOwnerAddress = document.getElementById("editOwnerAddress");
    const editYearOfManufacture = document.getElementById("editYearOfManufacture");

    editRegLicensePlate.value = reg.license_plate;
    editOwnerName.value = reg.owner_name;
    editOwnerAddress.value = reg.owner_address;
    editYearOfManufacture.value = reg.year_of_manufacture;

    editRegForm.classList.remove("hidden");

    editOwnerName.addEventListener("input", (e) => {
        const isValid = ownerNameRegex.test(e.target.value.trim());
        setFieldValidationStyle(e.target, isValid);
    });

    editOwnerAddress.addEventListener("input", (e) => {
        const isValid = ownerAddressRegex.test(e.target.value.trim());
        setFieldValidationStyle(e.target, isValid);
    });

    editYearOfManufacture.addEventListener("input", (e) => {
        const isValid = yearRegex.test(e.target.value.trim()) && e.target.value >= 1900 && e.target.value <= new Date().getFullYear();
        setFieldValidationStyle(e.target, isValid);
    });

    document.getElementById("submitEditReg").addEventListener("click", async () => {
        const updatedRegData = {
            owner_name: editOwnerName.value.trim(),
            owner_address: editOwnerAddress.value.trim(),
            year_of_manufacture: parseInt(editYearOfManufacture.value, 10),
        };

        const isOwnerNameValid = ownerNameRegex.test(updatedRegData.owner_name);
        const isOwnerAddressValid = ownerAddressRegex.test(updatedRegData.owner_address);
        const isYearValid = yearRegex.test(updatedRegData.year_of_manufacture) && updatedRegData.year_of_manufacture >= 1900 && updatedRegData.year_of_manufacture <= new Date().getFullYear();

        setFieldValidationStyle(editOwnerName, isOwnerNameValid);
        setFieldValidationStyle(editOwnerAddress, isOwnerAddressValid);
        setFieldValidationStyle(editYearOfManufacture, isYearValid);

        if (!isOwnerNameValid || !isOwnerAddressValid || !isYearValid) {
            alert("Пожалуйста, исправьте ошибки перед сохранением.");
            return;
        }

        const response = await authorizedFetch(`${API_BASE}/update_registration/${reg.license_plate}`, {
            method: "PUT",
            body: JSON.stringify(updatedRegData),
        });

        if (response && response.ok) {
            alert("Данные регистрации успешно обновлены.");
            editRegForm.classList.add("hidden");
            loadRegs();
        } else {
            alert("Ошибка при обновлении данных.");
        }
    });

    document.getElementById("cancelEditReg").addEventListener("click", () => {
        editRegForm.classList.add("hidden");
    });
}

document.getElementById("newRegLicensePlate").addEventListener("input", (e) => {
    const isValid = licensePlateRegex.test(e.target.value.trim());
    setFieldValidationStyle(e.target, isValid);
});

document.getElementById("newOwnerName").addEventListener("input", (e) => {
    const isValid = ownerNameRegex.test(e.target.value.trim());
    setFieldValidationStyle(e.target, isValid);
});

document.getElementById("newOwnerAddress").addEventListener("input", (e) => {
    const isValid = ownerAddressRegex.test(e.target.value.trim());
    setFieldValidationStyle(e.target, isValid);
});

document.getElementById("newYearOfManufacture").addEventListener("input", (e) => {
    const isValid = yearRegex.test(e.target.value.trim()) && e.target.value >= 1900 && e.target.value <= new Date().getFullYear();
    setFieldValidationStyle(e.target, isValid);
});

loadRegs();
