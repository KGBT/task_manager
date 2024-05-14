from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Concat
from django.forms import CharField
from django.db.models import CharField, Value
import typing

from task_manager import settings


# Create your models here.
class User(AbstractUser):

    def get_employees_for_choice(self) -> typing.List[tuple]:
        employees = self.userprofile.employees.values('id').annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField()))
        employees_list = []
        for emp in employees:
            employees_list.append((emp.get('id'), emp.get('full_name')))
        return employees_list

    @staticmethod
    def find_by_username(username: str) -> "User" or None:
        user = User.objects.filter(username=username)
        if user:
            return user[0]
        return None

    def exists_employees_by_username(self, username: str) -> bool:
        return self.userprofile.employees.filter(username=username).exists()

    def get_employees(self) -> "User" or None:
        employees = self.userprofile.employees.all()
        if employees:
            return employees
        return None

    @staticmethod
    def find_by_id(id: int) -> "User" or None:
        user = User.objects.filter(id=id)
        if user:
            return user[0]
        return None

    def get_full_name(self) -> str:
        return self.first_name + ' ' + self.last_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    employees = models.ManyToManyField(User, related_name='employees', blank=True)

    def __str__(self):
        return str(f'Пользователь: {self.user}\n работник: {self.employees}')

    @staticmethod
    def get_or_create(user: User) -> 'UserProfile':
        # print(f'userprofil получить или создать {UserProfile.objects.get_or_create(user=user)[0]}')
        return UserProfile.objects.get_or_create(user=user)[0]

    def add_employee(self, user: User) -> None:
        self.employees.add(user)

    @staticmethod
    def find_employees_by_user(user: User) -> "UserProfile" or None:
        user_profile = UserProfile.objects.filter(user=user)
        if user_profile:
            employees = user_profile[0].employees.all()
            if employees:
                return employees
            else:
                return None
        return None