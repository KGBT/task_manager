$(document).ready(function () {
    // отслеживаем событие отправки формы
    $('#employeeAdd').submit(function (event) {
        event.preventDefault();
        // создаем AJAX-вызов
        $.ajax({
            data: $(this).serialize(), // получаяем данные формы
            type: 'POST',
            url: "add-employee/",
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