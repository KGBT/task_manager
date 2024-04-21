from django.db import models
from django.db.models import F
from django.db.models.functions import Concat
from django.forms import CharField
from django.db.models import CharField, Value


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return 'Пользователь: ' + self.name + ' ' + self.surname + ' ' + self.username + ' ' + self.email

    # Метод для преобразования данных для поля Select
    @staticmethod
    def get_user_choices():
        users = User.objects.values('id').annotate(
            full_name=Concat('name', Value(' '), 'surname', output_field=CharField()))
        cleaned_users = []
        for i in range(len(users)):
            cleaned_users.append((users[i].get('id'), users[i].get('full_name')))
        print(cleaned_users)
        return cleaned_users

    @staticmethod
    def find_by_username(username):
        user=User.objects.filter(username=username)
        print(user)
        return user


class Employee(models.Model):
    user = models.ManyToManyField(User, related_name='employee', blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return 'Сотрудник: ' + self.name + ' ' + self.surname + ' ' + self.username + ' ' + self.email

    @staticmethod
    def create_and_save(user: User) -> None:
        emp = Employee(name=user.name, surname=user.surname, username=user.username, email=user.email)
        emp.save()
        # return emp

    @staticmethod
    def exists(username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @staticmethod
    def get_list_employee(username: str) -> list:
        return Employee.objects.filter(user__username=User.objects.get(username=username).username)

