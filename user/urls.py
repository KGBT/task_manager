from user import views
from django.urls import path

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('log_out/', views.log_out, name='log_out'),
]
