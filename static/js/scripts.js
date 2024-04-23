$(document).ready(function () {
    // отслеживаем событие отправки формы
    $('#employeeAdd').submit(function (event) {
        event.preventDefault();
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаяем данные формы
            type: 'POST',
            url: "add-employee/",
            // если успешно, то
            success: function (response) {
                event.target.reset();
                if (response.success == true) {
                    console.log(response);
                    const employeeAdd = document.getElementById('employeeAdd');
                    const alert = document.getElementById('alert-error-emp');
                    if (alert) {
                        alert.remove();
                    }

                    employeeAdd.insertAdjacentHTML('afterend', '<div class="alert alert-success alert-dismissible fade show" role="alert" id="alert-error-emp">\n' +
                        '                    Пользователь добавлен!\n' +
                        '                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
                        '                </div>')

                    const listEmp = document.getElementById('list-employees');

                    $('#list-employees').insertAdjacentHTML().insertAdjacentHTML('afterbegin',`<li class="list-group-item">${response.name} ${response.surname}</li>`); //временная затычка


                } else {
                    // $('#id_username').removeClass('is-invalid').addClass('is-valid');
                    // $('#usernameError').remove();
                    const employeeAdd = document.getElementById('employeeAdd');
                    const alert = document.getElementById('alert-error-emp');
                    if (alert) {
                        alert.remove();
                    }
                    employeeAdd.insertAdjacentHTML('afterend', '<div class="alert alert-danger alert-dismissible fade show" role="alert" id="alert-error-emp">\n' +
                        '                    Пользователь с таким именем не найден!\n' +
                        '                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n' +
                        '                </div>')

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