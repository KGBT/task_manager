from django.db import models
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

    def __str__(self):
        return 'Пользователь: ' + self.name + ' ' + self.surname + ' ' + self.username + ' ' + self.email

    # Метод для преобразования данных для формы поля ModelMultipleChoiceField
    def get_employees_for_choice(self) -> typing.List[tuple]:
        employees = self.userprofile.employees.values('id').annotate(
            full_name=Concat('name', Value(' '), 'surname', output_field=CharField()))
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
        return self.name + ' ' + self.surname


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


# Для сериализации объектов Django без пароля, вы можете использовать встроенные инструменты Django или сторонние библиотеки. Вот несколько способов сделать это:

# 1. **Использование встроенных инструментов Django:**
#
#     * Создайте сериализатор для вашей модели, используя встроенный класс `serializers.Serializer` или `serializers.ModelSerializer`.
#     * В сериализаторе определите поля, которые вы хотите сериализовать, и исключите поля, содержащие конфиденциальную информацию, такую как пароль.
#     * Используйте метод `serializers.serialize` для сериализации объекта модели в нужный формат (например, JSON).
#
# 2. **Использование сторонних библиотек:**
#
#     * Существует множество сторонних библиотек, которые могут помочь вам сериализовать объекты Django без пароля. Например, вы можете использовать библиотеку `django-rest-framework`, которая предоставляет мощные инструменты для создания RESTful API.
#
# Вот пример использования встроенных инструментов Django для сериализации объекта модели без пароля:
#
# ```python
# from django.core import serializers
# from myapp.models import User
#
# # Получаем объект модели
# user = User.objects.get(id=1)
#
# # Создаем сериализатор
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')
#
#     # Исключаем поле пароля
#     password = serializers.CharField(write_only=True)
#
# # Сериализуем объект в JSON
# serialized_user = UserSerializer(user).data
#
# # Выводим результат
# print(serialized_user)
# ```
#
# Этот код сериализует объект модели `User` без поля пароля и выводит результат на экран. Вы можете сохранить результат в файл или отправить его через API.
