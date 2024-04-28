from user import views
from django.urls import path
urlpatterns = [
    path('add-employee/', views.add_employee, name='add_employee'),
]