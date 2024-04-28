from django.http import JsonResponse
from django.shortcuts import render

from user.models import User, UserProfile


# Create your views here.


def add_employee(request):
    user_employee = User.find_by_username(request.POST['username'])

    context: dict = {'is_add': False, 'is_exist': False, 'is_not': False,
                     'message': ''}  # словарь со значениями для alerтов
    user_login = User.find_by_username(
        'nikitin')  # после реализации регистрации сделать получение пользователя через логин
    if user_employee:
        if user_login.exists_employees_by_username(user_employee.username):
            context['is_exist'] = True
            context['message'] = 'Сотрудник уже добавлен!'
        else:
            user_profile_employee = UserProfile.get_or_create(user_employee)
            user_profile_login = UserProfile.get_or_create(user_login)
            user_profile_employee.add_employee(user_login)
            user_profile_login.add_employee(user_employee)
            context['is_add'] = True
            context['message'] = 'Сотрудник добавлен!'
            context['full_name'] = user_employee.username + ' ' + user_employee.surname
    else:
        context['is_not'] = True
        context['message'] = 'Пользователь с таким именем не найден!'
    context['full_name'] = 'user_employee.username + ' ' + user_employee.surname'
    return JsonResponse(context)
