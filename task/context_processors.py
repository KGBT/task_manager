from task.models import UserTask
from user.models import User


def get_number_of_tasks(request):
    user = request.user
    user_log = User.find_by_username('terkin')
    inbox_count = UserTask.count_inbox_tasks(user_log.id)
    outbox_count = UserTask.count_outbox_tasks(user_log.id)
    tasks_count = UserTask.count_tasks(user_log.id)
    context = {'inbox_count':inbox_count, 'outbox_count':outbox_count, 'tasks_count':tasks_count}
    return context

