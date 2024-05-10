$(document).ready(function () {
    // отслеживаем событие отправки формы
    $('#employeeAdd').submit(function (event) {
        event.preventDefault();
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаяем данные формы
            type: 'POST',
            url: "add_employee/",
            datatype: 'json',
            // если успешно, то
            success: function (response) {
                event.target.reset();
                const employeeAdd = document.getElementById('employeeAdd');
                const alert = document.getElementById('alert-error-emp');
                if (alert) {
                    alert.remove();
                }
                if (response.is_add) {
                    const itemEmp = document.getElementById('item-employee');
                    const executors = document.getElementById('id_executors');
                    employeeAdd.insertAdjacentHTML('afterend', `<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-error-emp">${response.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);
                    itemEmp.insertAdjacentHTML('afterend', `<li class="list-group-item"> ${response.full_name} </li>`);
                    executors.insertAdjacentHTML('afterbegin', `<option value="${response.id}">${response.full_name} </option>`);

                } else if (response.is_exist) {
                    employeeAdd.insertAdjacentHTML('afterend', `<div class="alert alert-info alert-dismissible fade show" role="alert" id="alert-error-emp">${response.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);


                } else if (response.is_not) {
                    employeeAdd.insertAdjacentHTML('afterend', `<div class="alert alert-danger alert-dismissible fade show" role="alert" id="alert-error-emp">${response.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`)

                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})


$(document).ready(function () {

    // отслеживаем событие отправки формы
    $('#id_name').keyup(function () {

        // создаем AJAX-вызов
        $.ajax({
            datatype: 'json',
            data: $(this).serialize(), // получаяем данные формы
            url: "validate_task_name/",
            // если успешно, то
            success: function (response) {
                console.log('В ajax');

                if (response.is_empty == true || response.is_max_length == true) {
                    const alert = document.getElementById('nameError');
                    if (!alert) {
                        $('#id_name').addClass('is-invalid');
                        $('#id_name').after('<div class="invalid-feedback d-block" id="nameError">Это обятательное поле! Не более 50 символов.</div>');
                    }
                } else {

                    $('#id_name').removeClass('is-invalid');
                    $('#nameError').remove();
                }

            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})


$(document).ready(function () {

    // отслеживаем событие отправки формы
    $('#id_description').keyup(function () {

        // создаем AJAX-вызов
        $.ajax({
            datatype: 'json',
            data: $(this).serialize(), // получаяем данные формы
            url: "validate_description/",
            // если успешно, то
            success: function (response) {

                if (response.is_max_length == true) {
                    const alert = document.getElementById('nameError');
                    if (!alert) {
                        $('#id_description').addClass('is-invalid');
                        $('#id_description').after('<div class="invalid-feedback d-block" id="nameError">Не более 1000 символов.</div>');
                    }
                } else {

                    $('#id_description').removeClass('is-invalid');
                    $('#nameError').remove();
                }

            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})


$(document).ready(function () {

    const form = document.getElementById('addTask');
    const btn = document.getElementById('btn-addTask');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            btn.textContent = 'Отправка...';
            btn.disabled = true;
            console.log('in fetch')
            fetch('add_task/', {
                method: 'POST',
                body: new FormData(form)
            }).then((responce) => responce.json())
                .then((data) => {
                    // console.log('Какой-то ответ!');
                    // console.log(data);
                    if (data.ok === 'ok') {
                        e.target.reset();
                        const addTask = document.getElementById('addTask');
                        const alert = document.getElementById('alert-success');
                        if (alert) {
                            alert.remove();
                        }
                        addTask.insertAdjacentHTML('beforebegin', `<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-success">Задача отправлена!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);
                    }
                    btn.textContent = 'Отправить';
                    btn.disabled = false;
                });
        });
    }

});

$(document).ready(function () {
    console.log('До аякс');
    // отслеживаем событие отправки формы
    $('#id_message').keyup(function () {
        // создаем AJAX-вызов
        console.log('До аякс');
        $.ajax({
            datatype: 'json',
            data: $(this).serialize(), // получаяем данные формы
            url: "validate_message/",
            // если успешно, то
            success: function (response) {
                console.log('Успешно!');
                if (response.is_max_length_mess) {
                    const alert = document.getElementById('nameErrorMess');
                    if (!alert) {
                        $('#id_message').addClass('is-invalid');
                        $('#id_message').after('<div class="invalid-feedback d-block" id="nameErrorMess">Не более 1000 символов.</div>');
                    }
                } else {

                    $('#id_message').removeClass('is-invalid');
                    $('#nameErrorMess').remove();
                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
});
