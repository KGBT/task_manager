from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from user.forms import UserSignUpForm, UserSignInForm
from user.models import User, UserProfile


# Create your views here.


def sign_in(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            return redirect('/tasks')
    else:
        form = UserSignInForm()
    context = {'sign_in_form': form}
    return render(request, 'sign_in.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user_from_db = User.find_by_username(request.POST['username'])
            # if user_from_db:
            user_profile_employee = UserProfile.get_or_create(user)
            user_profile_employee.add_employee(user)
            login(request, user)
            return redirect('/tasks')
    else:
        form = UserSignUpForm()
    context = {'sign_up_form': form}

    return render(request, 'sign_up.html', context)


def log_out(request):
    logout(request)
    return redirect('/')
