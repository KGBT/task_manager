from django.contrib.auth import get_user_model

from task.models import UserTask
from user.models import User


# def get_number_of_tasks(request):
#     user_login = request.user
#     inbox_count = UserTask.count_inbox_tasks(user_login.id)
#     outbox_count = UserTask.count_outbox_tasks(user_login.id)
#     tasks_count = UserTask.count_tasks(user_login.id)
#     context = {'inbox_count':inbox_count, 'outbox_count':outbox_count, 'tasks_count':tasks_count}
#     return context

