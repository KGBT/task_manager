from django.http import HttpResponse
from django.shortcuts import render

from task.forms import TaskForm
from user.forms import UserForm


# Create your views here.
def index(request):
    context = {'TaskForm': TaskForm(), 'UserForm': UserForm()}
    return render(request, 'index.html', context=context)
