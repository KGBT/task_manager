import os
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from task.forms import TaskForm, PriorityForm, FileForm
from task.models import Task, Priority, Status, File, UserTask, FileAnswer

from user.models import User, UserProfile


# Create your views here.

@login_required
def tasks(request):
    user_login = request.user

    usertasks_tasks = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                     statuses=[Status.ACCEPTED, Status.FAILED])

    usertasks1 = (
        UserTask.objects.all().distinct('task'))


    paginator = Paginator(usertasks_tasks, per_page=8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'taskForm': TaskForm(user_login=user_login), 'priorityForm': PriorityForm(),
               'fileForm': FileForm(),
               'page_obj': page_obj
               }

    return render(request, 'objective/tasks.html', context)


@login_required
def tasks_inbox(request):
    user_login = request.user
    usertasks_inbox = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                     statuses=[Status.INBOX])
    paginator = Paginator(usertasks_inbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/inbox.html', context)


@login_required
def tasks_outbox(request):
    user_login = request.user
    usertasks_outbox = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                      statuses=[Status.OUTBOX, Status.COMPLETED,
                                                                                Status.FAILED, Status.ACCEPTED,
                                                                                Status.REJECTED])

    paginator = Paginator(usertasks_outbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/outbox.html', context)


@login_required
def tasks_archive(request):
    user_login = request.user
    usertasks_archive = UserTask.find_usertask_by_user_id_and_statuses(user_id=user_login.id,
                                                                       statuses=[Status.ARCHIVED])
    paginator = Paginator(usertasks_archive, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'objective/archive.html', context)


@login_required
def complete_task(request):
    task_id = request.POST.get('task_id')
    message = request.POST.get('message')
    usertasks = UserTask.find_usertasks_by_statuses(task_id=task_id, statuses=[Status.ACCEPTED, Status.FAILED])
    if usertasks:
        for usertask in usertasks:
            usertask.status.status = Status.COMPLETED
            usertask.status.save()
        if message and (usertasks[0].task.message is None or usertasks[0].task.message == ''):
            usertasks[0].task.message = message
            usertasks[0].task.save()
        if request.FILES:
            file_answer = FileAnswer.create_and_save_file(request.FILES['file_answer'])
            file_answer.add_task(usertasks[0].task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def accept_task(request, task_id):
    usertasks = UserTask.find_usertasks_by_statuses(task_id=task_id,
                                                    statuses=[Status.INBOX, Status.OUTBOX, Status.FAILED])
    if usertasks:
        for usertask in usertasks:
            usertask.status.status = Status.ACCEPTED
            usertask.status.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reject_task(request):
    task_id = request.POST.get('task_id')
    message = request.POST.get('message')
    usertasks = UserTask.find_usertasks_by_statuses(task_id=task_id,
                                                    statuses=[Status.INBOX, Status.OUTBOX, Status.FAILED])
    if usertasks:
        for usertask in usertasks:
            usertask.status.status = Status.REJECTED
            usertask.status.save()
        if message and (usertasks[0].task.message is None or usertasks[0].task.message == ''):
            usertasks[0].task.message = message
            usertasks[0].task.save()
        if request.FILES:
            file_answer = FileAnswer.create_and_save_file(request.FILES['file_answer'])
            file_answer.add_task(usertasks[0].task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_task(request, task_id):
    usertasks = UserTask.find_usertasks_by_statuses(task_id=task_id,
                                                    statuses=[Status.ACCEPTED, Status.FAILED, Status.INBOX,
                                                              Status.OUTBOX, Status.REJECTED, Status.COMPLETED])

    if usertasks:
        for usertask in usertasks:
            usertask.status.delete()
            usertask.delete()
        file = File.find_file_by_id_task(task_id)
        file_answer = FileAnswer.find_file_by_id_task(task_id)
        if file:
            file.delete()
        if file_answer:
            file_answer.delete()
        task = Task.find_task_by_id(task_id)
        task.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def archive_task(request, task_id):
    usertasks = UserTask.find_usertasks_by_statuses(task_id=task_id,
                                                    statuses=[Status.OUTBOX, Status.ACCEPTED, Status.FAILED,
                                                              Status.INBOX, Status.REJECTED, Status.COMPLETED])
    if usertasks:
        for usertask in usertasks:
            usertask.status.status = Status.ARCHIVED
            usertask.status.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Додeлать добавление работников обоим пользователям!
@login_required
def add_employee(request):
    user_employee = User.find_by_username(request.POST['username'])

    context: dict = {'is_add': False, 'is_exist': False, 'is_not': False,
                     'message': ''}  # словарь со значениями для alerтов
    user_login = request.user  # после реализации регистрации сделать получение пользователя через логин
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
    return JsonResponse(context)


@login_required
def add_task(request):
    if request.method == 'POST':
        user_login = request.user
        user_employee = User.find_by_id(request.POST['executors'])

        task = Task(name=request.POST['name'], description=request.POST['description'], date_start=date.today(),
                    initiator=user_login.get_full_name())  # Заменить на авторизованного пользователя

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


@login_required
def download_file(request, file_id):
    uploaded_file = File.find_file_by_id(file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(uploaded_file.file.name)
    return response


@login_required
def download_file_answer(request, file_id):
    uploaded_file = FileAnswer.find_file_by_id(file_id)
    response = HttpResponse(uploaded_file.file_answer, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(uploaded_file.file_answer.name)
    return response


@login_required
def validate_task_name(request):
    name = request.GET.get('name')
    context: dict = {'is_empty': False, 'is_max_length': False}
    if name == '':
        context['is_empty'] = True
    elif len(name) > 50:
        context['is_max_length'] = True
    return JsonResponse(context)


@login_required
def validate_description(request):
    description = request.GET.get('description')
    context: dict = {'is_max_length': False}
    if len(description) > 1000:
        context['is_max_length'] = True
    return JsonResponse(context)


@login_required
def validate_message(request):
    message = request.GET.get('message')
    context: dict = {'is_max_length_mess': False}
    if len(message) > 1000:
        context['is_max_length_mess'] = True
    return JsonResponse(context)
