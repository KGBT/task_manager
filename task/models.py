from django.db import models

from user.models import User


# Create your models here.

class Task(models.Model):
    users = models.ManyToManyField(User, through='UserTask')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField()



class Status(models.Model):
    status = models.CharField(max_length=15)
    message = models.TextField(max_length=1000, blank=True, null=True)


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)


class Priority(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Низкий'),
        (MEDIUM, 'Средний'),
        (HIGH, 'Высокий'),
    ]
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)


class File(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, null=True)
    path = models.FileField(upload_to='files/', null=True, blank=True)
