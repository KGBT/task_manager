from datetime import date

from django.db import models

from user.models import User


# Create your models here.

class Task(models.Model):
    users = models.ManyToManyField(User, through='UserTask')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    initiator = models.CharField(max_length=60, blank=True, null=True)
    priority = models.ForeignKey('Priority', on_delete=models.PROTECT)

    def __str__(self):
        return self.name + " " + self.description

    def add_date_end(self, date_end: 'date') -> None:
        self.date_end = date_end

    def add_priority(self, priority: 'Priority') -> None:
        self.priority_id = priority.id

    @staticmethod
    def get_tasks_with_priority_and_files(username: str, status: str) -> 'QuerySet':
        return Task.objects.filter(users__username=username,
                                   usertask__status__status=status).all().prefetch_related(
            'priority', 'file_set').order_by('id')  # объединение всех таблиц


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
    message = models.TextField(max_length=1000, blank=True, null=True)

    @staticmethod
    def create(status: str) -> 'Status':
        status = Status(status=status)
        status.save()
        return status

    def __str__(self):
        return self.status


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.task) + " " + str(self.status)

    @staticmethod
    def create_user_task(user: 'User', task: 'Task', status: 'Status') -> None:
        user_task = UserTask.objects.create(user=user, task=task, status=status)
        user_task.save()


class File(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

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
