import random

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import messages

# from task.forms import TaskForm, FileFieldForm, FileForm
from user.forms import UserForm
from user.models import User, Employee


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
    if request.POST:
        username = request.POST['username']
        print(username)
        user = User.find_by_username(username)
        print(user)
        if user:
            if not Employee.exists(username):
                Employee.create_and_save(user)
                # context['is_add'] = 'ADDED'
                messages.add_message(request, messages.SUCCESS, 'Сотрудник добавлен!')
            else:
                messages.add_message(request, messages.INFO, 'Сотрудник уже добавлен!')
                # context['is_add'] = 'EXIST'
        else:
            # context['is_add'] = 'NOTADDED'
            messages.add_message(request, messages.ERROR, 'Пользователь с таким именем не найден!')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    context = {'employees': Employee.get_list_employee('Kukumber')}
    return render(request, 'header.html', context)
