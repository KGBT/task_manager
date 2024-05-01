from django.urls import path

from task import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('scripts/', views.scripts, name='scripts'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_task/', views.add_task, name='add_task'),
    path('validate_task_name/', views.validate_task_name, name='validate_task_name'),
    path('validate_description/', views.validate_description, name='validate_description'),
    path('inbox/', views.tasks_inbox, name='tasks_inbox'),
    path('outbox/', views.tasks_outbox, name='tasks_outbox'),
    path('archive/', views.tasks_archive, name='tasks_archive'),
    path('download/<int:file_id>/',views.download_file,name='download_file'),
]
