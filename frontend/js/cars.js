const carsList = document.getElementById("carsList");
const addCarButton = document.getElementById("addCarButton");
const addCarForm = document.getElementById("addCarForm");
const submitAddCar = document.getElementById("submitAddCar");
const searchCarInput = document.getElementById("searchCarInput");
const searchCarButton = document.getElementById("searchCarButton");

const API_BASE = "/carsdb";
const API_REGS = "/regdb";
const makeRegex = /^[A-Za-zА-Яа-яЁё\s-]{1,50}$/;
const modelRegex = /^[A-Za-zА-Яа-яЁё0-9\s-]{1,50}$/;
const licensePlateRegex = /^[A-Za-zА-ЯЁ]{1}\d{3}[A-Za-zА-ЯЁ]{2}\d{2,3}$/;


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

async function loadCars() {
    const response = await authorizedFetch(`${API_BASE}/get_cars/`);

    if (!response || !response.ok) {
        console.error("Ошибка загрузки автомобилей:", response?.statusText);
        return;
    }

    const data = await response.json();

    if (data && Array.isArray(data.cars)) {
        const cars = data.cars;

        if (cars.length === 0) {
            carsList.innerHTML = "<li>Нет доступных автомобилей</li>";
        } else {
            carsList.innerHTML = "";
            cars.forEach(car => {
                const li = document.createElement("li");
                li.setAttribute("data-make", car.make);
                li.setAttribute("data-model", car.model);
                li.setAttribute("data-license", car.license_plate);
                li.innerHTML = `
                    <div class="car-info">
                        <strong>${car.make} ${car.model}</strong> 
                    </div>
                    <div class="button-row">
                        <button class="expand">Данные</button>
                        <button class="edit-car">Редактировать</button> <!-- Новая кнопка -->
                        <button class="find-reg">Найти регистрацию</button>
                        <button class="delete">Удалить</button>
                    </div>
                    <div class="car-details hidden">
                        <p>Марка: <strong>${car.make}</strong></p>
                        <p>Модель: <strong>${car.model}</strong></p>
                        <p>Номер: <strong>${car.license_plate}</strong></p>
                    </div>
                    <div class="reg-result hidden">
                        <p class="reg-info"></p>
                        <button class="add-reg hidden">Добавить регистрацию</button>
                        <button class="hide-reg hidden">Скрыть</button>
                    </div>
                `;
                carsList.appendChild(li);


                li.querySelector(".expand").addEventListener("click", () => {
                    const details = li.querySelector(".car-details");
                    details.classList.toggle("hidden");
                });

                li.querySelector(".edit-car").addEventListener("click", () => showEditCarForm(car));

                li.querySelector(".find-reg").addEventListener("click", async () => {
                    const licensePlate = car.license_plate;
                    const regResultDiv = li.querySelector(".reg-result");
                    const regInfoParagraph = regResultDiv.querySelector(".reg-info");
                    const addRegButton = regResultDiv.querySelector(".add-reg");
                    const hideRegButton = regResultDiv.querySelector(".hide-reg");


                    regInfoParagraph.textContent = "Загрузка...";
                    addRegButton.classList.add("hidden");
                    hideRegButton.classList.remove("hidden");

                    const regResponse = await authorizedFetch(`${API_REGS}/search_registrations/?query=${licensePlate}`);

                    regInfoParagraph.textContent = "";

                    if (regResponse) {
                        const data = await regResponse.json();
                        if (data && Array.isArray(data.registrations) && data.registrations.length > 0) {
                            const registration = data.registrations[0];
                            regInfoParagraph.innerHTML = `
                                <strong>Регистрация найдена:</strong><br>
                                Номер: ${registration.license_plate}<br>
                                Владелец: ${registration.owner_name}<br>
                                Адрес владельца: ${registration.owner_address}<br>
                                Год выпуска: ${registration.year_of_manufacture}
                            `;
                        } else {
                            regInfoParagraph.textContent = "Регистрация не найдена.";
                            addRegButton.classList.remove("hidden");
                        }
                    } else {
                        regInfoParagraph.textContent = "Ошибка при поиске регистрации.";
                    }

                    regResultDiv.classList.remove("hidden");


                    addRegButton.addEventListener("click", () => {
                        const licensePlate = car.license_plate;
                        window.location.href = `/static/html/registration.html?license_plate=${licensePlate}`;
                    });

                    hideRegButton.addEventListener("click", () => {
                        regResultDiv.classList.add("hidden");
                    });
                });

                li.querySelector(".delete").addEventListener("click", async () => {
                    const licensePlate = car.license_plate;

                    if (confirm("Удалить автомобиль? Обратите внимание: регистрация автомобиля также будет удалена!")) {
                        // Проверка наличия регистрации
                        const regCheckResponse = await authorizedFetch(`${API_REGS}/search_registrations/?query=${licensePlate}`);
                        if (regCheckResponse && regCheckResponse.ok) {
                            const regData = await regCheckResponse.json();
                            const registrations = regData.registrations;

                            if (Array.isArray(registrations) && registrations.length > 0) {
                                // Если регистрация существует, удаляем ее
                                const deleteRegResponse = await authorizedFetch(`${API_REGS}/delete_registration/${licensePlate}`, {
                                    method: "DELETE",
                                });

                                if (!deleteRegResponse || !deleteRegResponse.ok) {
                                    alert("Ошибка при удалении регистрации.");
                                    return;
                                }
                            }
                        }

                        // Удаление автомобиля
                        const deleteCarResponse = await authorizedFetch(`${API_BASE}/delete_car/${licensePlate}`, {
                            method: "DELETE",
                        });

                        if (deleteCarResponse && deleteCarResponse.ok) {
                            alert("Автомобиль успешно удален.");
                            loadCars(); // Обновляем список автомобилей
                        } else {
                            alert("Ошибка при удалении автомобиля.");
                        }
                    }
                });
            });
        }
    } else {
        console.error("Ответ сервера не содержит корректный список машин:", data);
        alert("Ошибка загрузки автомобилей.");
    }
}

function setFieldValidationStyle(input, isValid) {
    if (isValid) {
        input.style.border = "2px solid green";
    } else {
        input.style.border = "2px solid red";
    }
}

document.getElementById("newCarMake").addEventListener("input", (event) => {
    const isValid = makeRegex.test(event.target.value.trim());
    setFieldValidationStyle(event.target, isValid);
});

document.getElementById("newCarModel").addEventListener("input", (event) => {
    const isValid = modelRegex.test(event.target.value.trim());
    setFieldValidationStyle(event.target, isValid);
});

document.getElementById("newCarLicensePlate").addEventListener("input", (event) => {
    const isValid = licensePlateRegex.test(event.target.value.trim());
    setFieldValidationStyle(event.target, isValid);
});

addCarButton.addEventListener("click", () => {
    addCarForm.classList.toggle("hidden");
});


submitAddCar.addEventListener("click", async () => {
    const makeInput = document.getElementById("newCarMake");
    const modelInput = document.getElementById("newCarModel");
    const licensePlateInput = document.getElementById("newCarLicensePlate");

    const make = makeInput.value.trim();
    const model = modelInput.value.trim();
    const licensePlate = licensePlateInput.value.trim();

    const isMakeValid = makeRegex.test(make);
    const isModelValid = modelRegex.test(model);
    const isLicensePlateValid = licensePlateRegex.test(licensePlate);

    setFieldValidationStyle(makeInput, isMakeValid);
    setFieldValidationStyle(modelInput, isModelValid);
    setFieldValidationStyle(licensePlateInput, isLicensePlateValid);

    if (!isMakeValid || !isModelValid || !isLicensePlateValid) {
        alert("Пожалуйста, исправьте ошибки в форме перед добавлением автомобиля.");
        return;
    }

    const response = await authorizedFetch(`${API_BASE}/add_car/`, {
        method: "POST",
        body: JSON.stringify({ make, model, license_plate: licensePlate }),
    });

    if (response) {
        addCarForm.classList.add("hidden");
        loadCars();
    } else {
        alert("Ошибка добавления автомобиля.");
    }
});


searchCarButton.addEventListener("click", () => {
    const query = searchCarInput.value.toLowerCase();
    const cars = document.querySelectorAll("li");
    let found = false;

    const noResultsMessage = document.querySelector(".no-results");
    if (noResultsMessage) {
        noResultsMessage.remove();
    }
    cars.forEach(car => {
        const make = car.getAttribute("data-make") || "";
        const model = car.getAttribute("data-model") || "";
        const licensePlate = car.getAttribute("data-license") || "";

        if (make.toLowerCase().includes(query) || model.toLowerCase().includes(query) || licensePlate.toLowerCase().includes(query)) {
            car.style.display = "";
            found = true;
        } else {
            car.style.display = "none";
        }
    });

    if (!found && query != "") {
        if (!document.querySelector(".no-results")) {
            const noResultsMessage = document.createElement("li");
            noResultsMessage.classList.add("no-results");
            noResultsMessage.textContent = "Автомобили не найдены.";
            carsList.appendChild(noResultsMessage);
        }
    }
});

function showEditCarForm(car) {
    const editCarForm = document.getElementById("editCarForm");
    const editCarMake = document.getElementById("editCarMake");
    const editCarModel = document.getElementById("editCarModel");
    const editCarLicensePlate = document.getElementById("editCarLicensePlate");
    const submitEditCar = document.getElementById("submitEditCar");

    editCarMake.value = car.make;
    editCarModel.value = car.model;
    editCarLicensePlate.value = car.license_plate;

    editCarForm.classList.remove("hidden");

    editCarMake.addEventListener("input", (event) => {
        const isValid = makeRegex.test(event.target.value.trim());
        setFieldValidationStyle(event.target, isValid);
    });

    editCarModel.addEventListener("input", (event) => {
        const isValid = modelRegex.test(event.target.value.trim());
        setFieldValidationStyle(event.target, isValid);
    });

    editCarLicensePlate.addEventListener("input", (event) => {
        const isValid = licensePlateRegex.test(event.target.value.trim());
        setFieldValidationStyle(event.target, isValid);
    });

    // Отмена
    document.getElementById("cancelEditCar").addEventListener("click", () => {
        editCarForm.classList.add("hidden");
    });
}

document.getElementById("submitEditCar").addEventListener("click", async () => {
    const editCarForm = document.getElementById("editCarForm");
    const editCarMake = document.getElementById("editCarMake");
    const editCarModel = document.getElementById("editCarModel");
    const editCarLicensePlate = document.getElementById("editCarLicensePlate");

    const make = editCarMake.value.trim();
    const model = editCarModel.value.trim();
    const licensePlate = editCarLicensePlate.value.trim();

    const isMakeValid = makeRegex.test(make);
    const isModelValid = modelRegex.test(model);
    const isLicensePlateValid = licensePlateRegex.test(licensePlate);

    setFieldValidationStyle(editCarMake, isMakeValid);
    setFieldValidationStyle(editCarModel, isModelValid);
    setFieldValidationStyle(editCarLicensePlate, isLicensePlateValid);

    if (!isMakeValid || !isModelValid || !isLicensePlateValid) {
        alert("Пожалуйста, исправьте ошибки в форме перед сохранением изменений автомобиля.");
        return;
    }

    const updatedCar = {
        make: make,
        model: model,
    };

    const response = await authorizedFetch(`${API_BASE}/update_car/${licensePlate}`, {
        method: "PUT",
        body: JSON.stringify(updatedCar),
    });

    if (response) {
        alert("Данные автомобиля успешно обновлены.");
        editCarForm.classList.add("hidden");
        loadCars();
    } else {
        alert("Ошибка при обновлении данных автомобиля.");
    }
});

loadCars();
