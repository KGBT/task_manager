from django import template
from django.contrib.auth.context_processors import auth
from django.http import HttpResponse

from task.models import UserTask

register = template.Library()


# @register.simple_tag(name='get_number_of_tasks')
# def get_number_of_tasks(user_authenticate):
#     user_login = request.user
#     inbox_count = UserTask.count_inbox_tasks(user_login.id)
#     outbox_count = UserTask.count_outbox_tasks(user_login.id)
#     tasks_count = UserTask.count_tasks(user_login.id)
#     context = {'inbox_count': inbox_count, 'outbox_count': outbox_count, 'tasks_count': tasks_count}
#     return UserTask.count_inbox_tasks(user_login.id)


@register.inclusion_tag('tags/count_tasks.html')
def count_tasks(auth_user):
    counts = UserTask.count_tasks(auth_user.id)
    return {'counts': counts}


@register.inclusion_tag('tags/count_tasks.html')
def count_inbox_tasks(auth_user):
    counts = UserTask.count_inbox_tasks(auth_user.id)
    return {'counts': counts}


@register.inclusion_tag('tags/count_tasks.html')
def count_outbox_tasks(auth_user):
    counts = UserTask.count_outbox_tasks(auth_user.id)
    return {'counts': counts}
