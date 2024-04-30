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
                    employeeAdd.insertAdjacentHTML('afterend', `<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-error-emp">${response.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);
                    itemEmp.insertAdjacentHTML('afterend', `<li class="list-group-item"> ${response.full_name} </li>`);

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
                console.log('В ajax');
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
                    addTask.insertAdjacentHTML('beforebegin', `<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-error-emp">Задача отправлена!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);
                }
                btn.textContent = 'Отправить';
                btn.disabled = false;
            });
    });

    // отслеживаем событие отправки формы
    // $('#addTask').submit(function (event) {
    //     event.preventDefault();
    //     // создаем AJAX-вызов
    //     $.ajax({
    //         data: $(this).serialize(), // получаяем данные формы
    //         type: 'POST',
    //         url: "add_task/",
    //         // если успешно, то
    //         success: function (response) {
    //             console.log('В ajax post');
    //             event.target.reset();
    //             const addTask = document.getElementById('addTask');
    //             addTask.insertAdjacentHTML('beforebegin', `<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-error-emp">Задача отправлена!
    //             <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`);
    //
    //         },
    //         // если ошибка, то
    //         error: function (response) {
    //             // предупредим об ошибке
    //             console.log(response.responseJSON.errors)
    //         }
    //     });
    //     return false;
    // });
})