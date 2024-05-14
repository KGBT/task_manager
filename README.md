# Task_manager
Таск-менеджер - это приложение, предназначенное для управления задачами, организации рабочего времени и контроля
выполнения задач. Позволяет расставлять приоритеты, отслеживать процесс выполнения задач.

## Чтобы развернуть сервер на вашем устройстве:

1. Установить PostgreSQL
2. Установить Python 3.12.2
3. Открыть командную строку cmd
4. Перейти в папку с проектом cd 'path\task_manager'
5. Выполнить команду pip install -r 'requirements.txt'
6. Перейти в настроечный файл task_manager\settings.py
7. Найти пункт DATABASES и изменить настройки на свои
8. <pre>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager',
        'USER': 'Имя пользователя PostgreSQL', #По умолчанию пользователь: postgres
        'PASSWORD': 'Пароль, заданный при установке PostgreSQL',
        'HOST': 'HOST', #Если на своей машине: localhost
        'PORT': PORT #Порт заданный при установке. По умолчанию: 5432
    }}</pre>
9. Запустить проект командой py manage.py runserver

