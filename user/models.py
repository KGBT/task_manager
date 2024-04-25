from django.db import models
from django.db.models import F
from django.db.models.functions import Concat
from django.forms import CharField
from django.db.models import CharField, Value
import typing


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=1000)

    def __dict__(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'email': self.email,
        }

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
    def find_by_username(username: str) -> "User" or None:
        user = User.objects.filter(username=username)
        users = User.objects.all()
        # print(f'from models {user}')
        # print(f'from models all {users}')
        if user:
            return user[0]
        return None

    # @staticmethod
    # def set_employees(user, employee):
    #     user.employee_set.add(employee)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    employees = models.ManyToManyField(User, related_name='employees', blank=True)

    def __str__(self):
        return str(f'Пользователь: {self.user}\n работник: {self.employees}')

    # def __dict__(self):
    #     return {'user': self.user, 'employees': self.employees}

    @staticmethod
    def get_or_create(user: User) -> 'UserProfile':
        print(f'userprofil получить или создать {UserProfile.objects.get_or_create(user=user)[0]}')
        return UserProfile.objects.get_or_create(user=user)[0]

    @staticmethod
    def add_employee(user_profile, user: User) -> None:
        user_profile.employees.add(user)

    @staticmethod
    def find_employees_by_user(user: User) -> "UserProfile" or None:
        user_profile = UserProfile.objects.filter(user=user)
        print(f'userprofil поиск {user_profile}')
        if user_profile:
            return user_profile
        return None

# class Employee(models.Model):
#     user = models.ManyToManyField(User, related_name='employee', blank=True)
#     name = models.CharField(max_length=30)
#     surname = models.CharField(max_length=30)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#
#     def __str__(self):
#         return 'Сотрудник: ' + self.name + ' ' + self.surname + ' ' + self.username + ' ' + self.email
#
#     @staticmethod
#     def create_and_save(user: User):  # как сделать Employee
#         emp = Employee(name=user.name, surname=user.surname, username=user.username, email=user.email)
#         emp.save()
#         return emp
#
#     @staticmethod
#     def exists(username: str) -> bool:
#         return Employee.objects.filter(username=username).exists()
#
#     @staticmethod
#     def get_list_employee(username: str) -> list:
#         return Employee.objects.filter(user__username=User.objects.get(username=username).username)
#
#     @staticmethod
#     def find_by_username(username):
#         emp = Employee.objects.filter(username=username)[0]
#         return emp
#
#     @staticmethod
#     def set_user(employee, user):
#         employee.user_set.add(user)
#
