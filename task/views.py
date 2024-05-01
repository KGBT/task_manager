from datetime import date

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from task.forms import TaskForm, PriorityForm, FileForm
from task.models import Task, Priority, Status, File, UserTask

from user.models import User, UserProfile


# Create your views here.


def tasks(request):
    user_login = User.find_by_username('nikitin')
    tasks = Task.get_tasks_with_priority_and_files('terkin', Status.INBOX)
    paginator = Paginator(tasks, per_page=8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(tasks.__dict__)

    context = {'taskForm': TaskForm(user_login=user_login), 'priorityForm': PriorityForm(),
               'fileForm': FileForm(),
               'employees': user_login.get_employees(), 'tasks': tasks, 'page_obj': page_obj}

    return render(request, 'tasks.html', context)


def tasks_inbox(request):
    user_login = User.find_by_username('nikitin')
    tasks_inbox = Task.get_tasks_with_priority_and_files('terkin', Status.INBOX)
    paginator = Paginator(tasks_inbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employees': user_login.get_employees(), 'page_obj': page_obj}

    return render(request, 'inbox.html', context)


def tasks_outbox(request):
    user_login = User.find_by_username('nikitin')
    tasks_outbox = Task.get_tasks_with_priority_and_files('terkin', Status.INBOX)
    paginator = Paginator(tasks_outbox, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employees': user_login.get_employees(), 'page_obj': page_obj}

    return render(request, 'outbox.html', context)


def tasks_archive(request):
    user_login = User.find_by_username('nikitin')
    tasks_archive = Task.get_tasks_with_priority_and_files('terkin', Status.INBOX)
    paginator = Paginator(tasks_archive, per_page=9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employees': user_login.get_employees(), 'page_obj': page_obj}

    return render(request, 'archive.html', context)


def download_file(request, file_id):
    uploaded_file = File.find_file_by_id(file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(uploaded_file.file.name)
    return response

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
    # context['full_name'] = 'user_employee.username + ' ' + user_employee.surname'
    return JsonResponse(context)


def add_task(request):
    print(request.POST)
    print(request.FILES)
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

# def index(request):
#     # if request.POST:
#     #     username = request.POST['username']
#     #     user = User.find_by_username(username)
#     #     if user:
#     #         if not Employee.exists(username):
#     #             emp = Employee.create_and_save(user)
#     #         else:
#     #             emp = Employee.find_by_username(username)
#     #         user_temp = User.find_by_username('nikitin')
#     #         Employee.set_user(emp, user_temp)
#     #         messages.add_message(request, messages.SUCCESS, 'Сотрудник добавлен!')
#     #     else:
#     #         messages.add_message(request, messages.ERROR, 'Пользователь с таким именем не найден!')
#     #     return redirect(request.META.get('HTTP_REFERER', '/'))
#     user_login = User.find_by_username('nikitin')
#     context = {'employees': user_login.get_employees()}
#     user = User.objects.filter(name='ivan')
#     if not user:
#         user_ivan = User(name='ivan', surname='nikitin', username='nikitin', email='nikitin@.ru', password='<PASSWORD>')
#         user_ivan.save()
#         user_alex = User(name='alex', surname='terkin', username='terkin', email='terkin@.ru', password='<PASSWORD>')
#         user_alex.save()
#     return render(request, 'header.html', context)


# user_profile_employee = UserProfile.get_or_create(user_login)
# UserProfile.add_employee(user_profile_employee, user_login)
# print(f'работник из вью {user_login.userprofile.employees.all()}',
#       )  # доступ к работникам
# print(type(user_login.userprofile.employees.all()))


# name_emp = user_login.userprofile.employees.filter(username='nikitin').values().annotate(
#     full_name=Concat('name', Value(' '), 'surname', output_field=CharField()))
# full_name = name_emp[0]['full_name']
# print(full_name, 'asdsasdasdasdas')
# context['full_name'] = full_name
# context['user'] = serializers.serialize('json',[user_login])
