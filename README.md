# Task_manager
Таск-менеджер - это приложение, предназначенное для управления задачами, организации рабочего времени и контроля
выполнения задач. Позволяет расставлять приоритеты, отслеживать процесс выполнения задач.

## Чтобы развернуть сервер на вашем устройстве:

1. Установить PostgreSQL 15.7 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Зайти в pgAdmin
3. Создать базу данных task_manager
4. Установить Python 3.12.2 https://www.python.org/downloads/release/python-3122/
5. Открыть командную строку cmd
6. Перейти в папку с проектом cd 'path\task_manager'
7. Выполнить команду pip install -r 'requirements.txt'
8. Перейти в настроечный файл task_manager\settings.py
9. Найти пункт DATABASES и изменить настройки на свои
10. <pre>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager',
        'USER': 'Имя пользователя PostgreSQL', #По умолчанию пользователь: postgres
        'PASSWORD': 'Пароль, заданный при установке PostgreSQL',
        'HOST': 'HOST', #Если на своей машине: localhost
        'PORT': PORT #Порт заданный при установке. По умолчанию: 5432
    }}</pre>
11. Выполнить в командной строке python manage.py makemigrations
12. Выполнить в командной строке py manage.py migrate   
13. Запустить проект командой py manage.py runserver


