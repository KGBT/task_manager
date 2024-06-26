from django.urls import path

from task import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    # path('scripts/', views.scripts, name='scripts'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('inbox/add_employee/', views.add_employee, name='add_employee'),
    path('outbox/add_employee/', views.add_employee, name='add_employee'),
    path('archive/add_employee/', views.add_employee, name='add_employee'),
    path('add_task/', views.add_task, name='add_task'),
    path('validate_task_name/', views.validate_task_name, name='validate_task_name'),
    path('validate_description/', views.validate_description, name='validate_description'),
    path('validate_message/', views.validate_message, name='validate_message'),
    path('inbox/', views.tasks_inbox, name='tasks_inbox'),
    path('outbox/', views.tasks_outbox, name='tasks_outbox'),
    path('archive/', views.tasks_archive, name='tasks_archive'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('download_file_answer/<int:file_id>/', views.download_file_answer, name='download_file_answer'),
    path('complete/', views.complete_task, name='complete_task'),
    path('rejected/', views.reject_task, name='reject_task'),
    path('accept/<int:task_id>/', views.accept_task, name='accept_task'),
    path('archive/<int:task_id>/', views.archive_task, name='archive_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
