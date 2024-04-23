from django.urls import path

from task import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-employee/', views.add_employee, name='add_employee'),
]
