from datetime import date

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import register

from task.forms import TaskForm, PriorityForm, FileForm
from task.models import Task, Priority, Status, File, UserTask

from user.models import User, UserProfile


# Create your views here.


def tasks(request):
    user_login = User.find_by_username('terkin')
    # tasks = Task.get_tasks_with_priority_and_files('terkin', [Status.ACCEPTED])
    usertasks_tasks = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                     statuses=[Status.ACCEPTED, Status.FAILED])

    user_login = User.find_by_username('nikitin')
    paginator = Paginator(usertasks_tasks, per_page=8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'taskForm': TaskForm(user_login=user_login), 'priorityForm': PriorityForm(),
               'fileForm': FileForm(),
               'page_obj': page_obj
               }

    return render(request, 'objective/tasks.html', context)


def tasks_inbox(request):
    user_login = User.find_by_username('terkin')
    usertasks_inbox = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id, statuses=[Status.INBOX])
    paginator = Paginator(usertasks_inbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/inbox.html', context)


def tasks_outbox(request):
    user_login = User.find_by_username('nikitin')
    usertasks_outbox = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                      statuses=[Status.OUTBOX, Status.COMPLETED,
                                                                                Status.FAILED])

    paginator = Paginator(usertasks_outbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/outbox.html', context)


def tasks_archive(request):
    user_login = User.find_by_username('nikitin')
    usertasks_archive = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                       statuses=[Status.ARCHIVED])
    paginator = Paginator(usertasks_archive, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/archive.html', context)


def download_file(request, file_id):
    uploaded_file = File.find_file_by_id(file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(uploaded_file.file.name)
    return response


def complete_task(request):
    user_login = User.find_by_username('nikitin')

    # usertask = UserTask.find_status_by_task_and_status(task_id=task_id, status=Status.COMPLETED)
    print(request.POST)
    # print('Айдишник таски' + request.POST['task_id'])
    # print('Сообщение' + request.POST['message'])
    # if usertask:
    #     usertask.status.status = Status.OUTBOX
    #     usertask.status.save()
    # print(usertask)

    return HttpResponseRedirect('/tasks')


def delete_task(request, task_id):
    delete_user_tasks = UserTask.find_user_tasks_by_id_task_for_delete(task_id=task_id)

    print(delete_user_tasks)
    task = Task.find_task_by_id(task_id)
    task.delete()
    if delete_user_tasks:
        for user_task in delete_user_tasks:
            user_task.status.delete()
            user_task.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def archive_task(request, task_id):
    user_task_statuses = UserTask.find_statuses_by_task_and_statuses(task_id=task_id,
                                                                     statuses=[Status.OUTBOX, Status.ACCEPTED])
    if user_task_statuses:
        for user_task_status in user_task_statuses:
            user_task_status.status.status = Status.ARCHIVED
            user_task_status.status.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def accept_task(request, task_id):
    user_task_status = UserTask.find_status_by_task_and_status(task_id=task_id, status=Status.INBOX)
    if user_task_status:
        user_task_status.status.status = Status.ACCEPTED
        user_task_status.status.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reject_task(request):
    task_id = request.POST.get('task_id')
    message = request.POST.get('message')
    user_tasks = UserTask.find_user_tasks_by_task_id(task_id=task_id)
    if user_tasks:
        if message:
            user_tasks[0].task.message = message
            user_tasks[0].task.save()
        for user_task in user_tasks:
            user_task.status.status = Status.REJECTED
            user_task.status.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def validate_task_name(request):
    name = request.GET.get('name')
    context: dict = {'is_empty': False, 'is_max_length': False}
    if name == '':
        context['is_empty'] = True
    elif len(name) > 50:
        context['is_max_length'] = True
    return JsonResponse(context)


def validate_description(request):
    description = request.GET.get('description')
    context: dict = {'is_max_length': False}
    if len(description) > 1000:
        context['is_max_length'] = True
    return JsonResponse(context)


def validate_message(request):
    message = request.GET.get('message')
    context: dict = {'is_max_length_mess': False}
    if len(message) > 1000:
        context['is_max_length_mess'] = True
    return JsonResponse(context)


def scripts(request):
    user = User.find_by_username(username='nikitin')
    if not user:
        user_ivan = User(name='ivan', surname='nikitin', username='nikitin', email='nikitin@.ru', password='<PASSWORD>')
        user_ivan.save()
        user_alex = User(name='alex', surname='terkin', username='terkin', email='terkin@.ru', password='<PASSWORD>')
        user_alex.save()
    user_profile_employee = UserProfile.get_or_create(user)
    user_profile_employee.add_employee(user)
    return HttpResponse('ok')


# Доднлать добавление работников обоим пользователям!
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
            context['id'] = user_employee.id
            context['full_name'] = user_employee.username + ' ' + user_employee.surname
    else:
        context['is_not'] = True
        context['message'] = 'Пользователь с таким именем не найден!'
    # context['full_name'] = 'user_employee.username + ' ' + user_employee.surname'
    return JsonResponse(context)


def add_task(request):
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST':
        user_login = User.find_by_username('nikitin')
        user_employee = User.find_by_id(request.POST['executors'])

        task = Task(name=request.POST['name'], description=request.POST['description'], date_start=date.today(),
                    initiator='ivan nikitin')  # Заменить на авторизованного пользователя

        priority = Priority.get_or_create(request.POST['priority'])
        task.add_priority(priority)

        date_end = request.POST['date_end']
        if date_end:
            task.add_date_end(date_end)

        task.save()

        if request.FILES:
            task_file = File.create_and_save_file(request.FILES['file'])
            task_file.add_task(task)

        status_for_login = Status.create(Status.OUTBOX)
        status_for_employee = Status.create(Status.INBOX)

        UserTask.create_user_task(user_login, task, status_for_login)
        UserTask.create_user_task(user_employee, task, status_for_employee)

    return JsonResponse({'ok': 'ok'})

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
