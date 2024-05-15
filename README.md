# Task_manager
Таск-менеджер - это приложение, предназначенное для управления задачами, организации рабочего времени и контроля
выполнения задач. Позволяет расставлять приоритеты, отслеживать процесс выполнения задач.

## Чтобы развернуть сервер на вашем устройстве:

1. Установить PostgreSQL 15.7 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Зайти в pgAdmin на своем компьютере с помощью пароля, указанного при установке.
3. Databases -> Правая клавиша мышки -> Create Database -> Database - Вводим название базы данных task_manager -> Жмем кнопочку Save
5. Установить Python 3.12.2 https://www.python.org/downloads/release/python-3122/
6. Открыть командную строку cmd
7. Перейти в папку с проектом cd 'path\task_manager'
8. Выполнить команду pip install -r 'requirements.txt'
9. Перейти в настроечный файл task_manager\settings.py
10. Найти пункт DATABASES и изменить настройки на свои
11. <pre>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager',
        'USER': 'Имя пользователя PostgreSQL', #По умолчанию пользователь: postgres
        'PASSWORD': 'Пароль, заданный при установке PostgreSQL',
        'HOST': 'HOST', #Если на своей машине: localhost
        'PORT': PORT #Порт заданный при установке. По умолчанию: 5432
    }}</pre>
12. Выполнить в командной строке python manage.py makemigrations
13. Выполнить в командной строке py manage.py migrate   
14. Запустить проект командой py manage.py runserver


