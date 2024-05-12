import datetime
from datetime import date

from django.db import models

from task_manager import settings
from user.models import User


# Create your models here.

class Task(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserTask')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    initiator = models.CharField(max_length=60, blank=True, null=True)
    message = models.TextField(max_length=1000, blank=True, null=True)
    priority = models.ForeignKey('Priority', on_delete=models.PROTECT)

    def __str__(self):
        return self.name + " " + self.description

    @staticmethod
    def find_task_by_id(task_id: int) -> 'Task' or None:
        task = Task.objects.filter(id=task_id)
        if task:
            return task[0]
        return None

    def add_date_end(self, date_end: 'date') -> None:
        self.date_end = date_end

    def add_priority(self, priority: 'Priority') -> None:
        self.priority_id = priority.id


class Priority(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Низкий'),
        (MEDIUM, 'Средний'),
        (HIGH, 'Высокий'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)

    @staticmethod
    def get_or_create(priority: str) -> 'Priority':
        return Priority.objects.get_or_create(priority=priority)[0]

    def __str__(self):
        return str(self.priority)


class Status(models.Model):
    INBOX = 'inbox'  # входящие задачи
    OUTBOX = 'outbox'  # исходящие задачи
    COMPLETED = 'completed'  # заверщенные задачи
    FAILED = 'failed'  # просроченные
    REJECTED = 'rejected'  # отклоненные
    ACCEPTED = 'accepted'  # принятые
    ARCHIVED = 'archived'  # архивные
    STATUS_CHOICES = (
        (INBOX, 'Inbox'),
        (OUTBOX, 'Outbox'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (ARCHIVED, 'Archived'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=INBOX)

    @staticmethod
    def create(status: str) -> 'Status':
        status = Status(status=status)
        status.save()
        return status

    def __str__(self):
        return self.status


class UserTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.task) + " " + str(self.status)

    @staticmethod
    def create_user_task(user: 'User', task: 'Task', status: 'Status') -> None:
        user_task = UserTask.objects.create(user=user, task=task, status=status)
        user_task.save()

    @staticmethod
    def find_usertasks_by_statuses(task_id: int, statuses: [str]) -> 'UserTask' or None:
        usertasks = UserTask.objects.filter(task_id=task_id, status__status__in=statuses).all()
        if usertasks:
            return usertasks
        return None

    @staticmethod
    def __get_count_tasks(user_id: int, statuses: [str]) -> int:
        return UserTask.objects.filter(status__status__in=statuses, user_id=user_id).count()

    @staticmethod
    def count_tasks(user_id: int) -> int:
        return UserTask.__get_count_tasks(user_id, [Status.ACCEPTED, Status.FAILED])

    @staticmethod
    def count_inbox_tasks(user_id: int) -> int:
        return UserTask.__get_count_tasks(user_id, [Status.INBOX])

    @staticmethod
    def count_outbox_tasks(user_id: int) -> int:
        return UserTask.__get_count_tasks(user_id, [Status.OUTBOX, Status.COMPLETED,
                                                    Status.FAILED, Status.ACCEPTED,
                                                    Status.REJECTED])

    @staticmethod
    def find_usertask_by_user_id_and_statuses(user_id: int, statuses: [str]) -> 'QuerySet':
        usertasks = (UserTask.objects.filter(user_id=user_id, status__status__in=statuses).all().distinct()
                     .prefetch_related('task', 'task__priority', 'task__file_set').order_by('-task__date_start'))
        if Status.FAILED in statuses:
            for usertask in usertasks:
                if usertask.task.date_end:
                    if usertask.task.date_end < datetime.date.today():
                        usertask.status.status = Status.FAILED
                        usertask.status.save()
        return usertasks


class File(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.file)

    @staticmethod
    def create_and_save_file(file: 'File') -> 'File':
        file = File(file=file)
        file.save()
        return file

    def add_task(self, task: 'Task') -> None:
        self.task_id = task.id
        self.save()

    @staticmethod
    def find_file_by_id(file_id: int) -> 'File' or None:
        file = File.objects.filter(id=file_id)
        if file:
            return file[0]
        return None

    @staticmethod
    def find_file_by_id_task(task_id: int) -> 'File' or None:
        file = File.objects.filter(task_id=task_id)
        if file:
            return file[0]
        return None
