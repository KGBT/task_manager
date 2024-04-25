import json
import random

from django.core.exceptions import ValidationError
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import messages
from django.db.models import CharField, Value
# from task.forms import TaskForm, FileFieldForm, FileForm
from user.forms import UserForm
from user.models import User, UserProfile


# Create your views here.
#
# class FileFieldFormView(FormView):
#     form_class = FileFieldForm
#     template_name = "upload.html"  # Replace with your template.
#     success_url = "..."  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         files = form.cleaned_data["file_field"]
#         for f in files:
#             ...  # спросить у Владислава
#         return super().form_valid()
#

def index(request):
    # if request.POST:
    #     username = request.POST['username']
    #     user = User.find_by_username(username)
    #     if user:
    #         if not Employee.exists(username):
    #             emp = Employee.create_and_save(user)
    #         else:
    #             emp = Employee.find_by_username(username)
    #         user_temp = User.find_by_username('nikitin')
    #         Employee.set_user(emp, user_temp)
    #         messages.add_message(request, messages.SUCCESS, 'Сотрудник добавлен!')
    #     else:
    #         messages.add_message(request, messages.ERROR, 'Пользователь с таким именем не найден!')
    #     return redirect(request.META.get('HTTP_REFERER', '/'))
    # context = {'employees': Employee.get_list_employee('nikitin')}
    user = User.objects.filter(name='ivan')
    if not user:
        user_ivan = User(name='ivan', surname='nikitin', username='nikitin', email='nikitin@.ru', password='<PASSWORD>')
        user_ivan.save()
        user_alex = User(name='alex', surname='terkin', username='terkin', email='terkin@.ru', password='<PASSWORD>')
        user_alex.save()
    return render(request, 'header.html')


def add_employee(request):
    # чтобы использовать объекты их необходимо сериализовать
    username = request.POST['username']

    user_employee = User.find_by_username(username)

    context: dict = {}
    user_login = User.find_by_username(
        'nikitin')  # после реализации регистрации сделать получение пользователя через логин
    if user_employee:

        print(f'работник из вью {user_login.userprofile.employees.all()}',
              )  # доступ к работникам
        print(type(user_login.userprofile.employees.all()))
        user_profile_employee = UserProfile.get_or_create(user_employee)
        user_profile_login = UserProfile.get_or_create(user_login)
        UserProfile.add_employee(user_profile_employee, user_login)
        UserProfile.add_employee(user_profile_login, user_employee)

        # user_profile_employee = UserProfile.get_or_create(user_login)
        # UserProfile.add_employee(user_profile_employee, user_login)
        context['success'] = True
    else:
        context['success'] = False
    name_emp = user_login.userprofile.employees.filter(username='nikitin').values().annotate(
            full_name=Concat('name', Value(' '), 'surname', output_field=CharField()))
    full_name = name_emp[0]['full_name']
    print(full_name, 'asdsasdasdasdas')
    context['full_name'] = full_name
    return JsonResponse(context)
