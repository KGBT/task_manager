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
    $('#id_name').keyup(function (e) {

        $.ajax({
                datatype: 'json',
                data: {'name': e.target.value},
                url: "validate_task_name/",
                success: function (response) {
                    const btn = document.getElementById('btn-addTask');
                    if (response.is_empty || response.is_max_length) {
                        const alert = document.getElementById('nameError');
                        e.target.classList.add('is-invalid');
                        btn.disabled = true;
                        if (!alert) {
                            e.target.insertAdjacentHTML('afterend', '<div class="invalid-feedback d-block" id="nameError">Это обятательное поле! Не более 50 символов.</div>');
                        }
                    } else {
                        if (e.target.classList.contains('is-invalid')) {
                            btn.disabled = false;
                            e.target.classList.remove('is-invalid');
                            $('#nameError').remove();
                        }
                    }
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });

    });
})


$(document).ready(function () {

    // отслеживаем событие отправки формы
    $('#id_description').keyup(function (e) {
         $.ajax({
                datatype: 'json',
                data: {'description': e.target.value},
                url: "validate_description/",
                success: function (response) {
                    const btn = document.getElementById('btn-addTask');
                    if (response.is_max_length) {
                        const alert = document.getElementById('nameError');
                        e.target.classList.add('is-invalid');
                        btn.disabled = true;
                        if (!alert) {
                            e.target.insertAdjacentHTML('afterend', '<div class="invalid-feedback d-block" id="nameError">Не более 1000 символов.</div>');
                        }
                    } else {
                        if (e.target.classList.contains('is-invalid')) {
                            btn.disabled = false;
                            e.target.classList.remove('is-invalid');
                            $('#nameError').remove();
                        }
                    }
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
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

})


$(document).ready(function () {
    const messages = document.getElementsByName('message');
    for (const message of messages) {
        message.addEventListener('keyup', (e) => {

            $.ajax({
                datatype: 'json',
                data: {'message': e.target.value},
                url: "validate_message/",
                success: function (response) {
                    const btn = document.getElementById('btn-complete');
                    if (response.is_max_length_mess) {
                        const alert = document.getElementById('nameErrorMess');
                        e.target.classList.add('is-invalid');
                        btn.disabled = true;
                        if (!alert) {
                            e.target.insertAdjacentHTML('afterend', '<div class="invalid-feedback d-block" id="nameErrorMess">Не более 1000 символов.</div>');
                        }
                    } else {
                        if (e.target.classList.contains('is-invalid')) {
                            btn.disabled = false;
                            e.target.classList.remove('is-invalid');
                            $('#nameErrorMess').remove();
                        }
                    }
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        });
    }
});


// $.ajax({
//         datatype: 'json',
//         data: $(this).serialize(),
//         url: "validate_message/",
//
//         success: function (response) {
//             if (response.is_max_length_mess) {
//                 const alert = document.getElementById('nameErrorMess');
//                 this.classList.add('is-invalid');
//                 if (!alert) {
//                     this.after('<div class="invalid-feedback d-block" id="nameErrorMess">Не более 1000 символов.</div>');
//                 }
//             } else {
//                 if (this.classList.contains('is-invalid')) {
//                     this.classList.remove('is-invalid');
//                     $('#nameErrorMess').remove();
//                 }
//             }
//         },
//         // если ошибка, то
//         error: function (response) {
//             // предупредим об ошибке
//             console.log(response.responseJSON.errors)
//         }
//     });
//     return false;

// onkeyup(function () {
//
//             $.ajax({
//                 datatype: 'json',
//                 data: message.serialize(),
//                 url: "validate_message/",
//
//                 success: function (response) {
//
//
//                     if (response.is_max_length_mess == true) {
//                         const alert = document.getElementById('nameErrorMess');
//                         if (!alert) {
//                             message.addClass('is-invalid');
//                             message.after('<div class="invalid-feedback d-block" id="nameErrorMess">Не более 1000 символов.</div>');
//                         }
//                     } else {
//
//                         message.removeClass('is-invalid');
//                         $('#nameErrorMess').remove();
//                     }
//                 },
//                 // если ошибка, то
//                 error: function (response) {
//                     // предупредим об ошибке
//                     console.log(response.responseJSON.errors)
//                 }
//             });
//             return false;
//         });

// $(document).ready(function () {
//
//     const acceptTask = document.getElementById('acceptTask')
//     console.log('В скрипте!')
//     acceptTask.forEach(function (acceptTask) {
//         acceptTask.addEventListener('click', function () {
//             $.ajax({
//                 url: `${acceptTask.getAttribute('href')}`,
//                 type: 'GET',
//                 success: function (response) {
//                     console.log('Принято!')
//                 },
//                 // если ошибка, то
//                 error: function (response) {
//                     // предупредим об ошибке
//                     console.log(response.errors)
//                 }
//             });
//             return false;
//         });
//     })
// })

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