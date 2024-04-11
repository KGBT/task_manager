import random

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from task.forms import TaskForm, FileFieldForm, FileForm
from user.forms import UserForm
from user.models import User


# Create your views here.

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"  # Replace with your template.
    success_url = "..."  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            ...  # спросить у Владислава
        return super().form_valid()


def index(request):
    if request.method == 'POST':
        pass
    # for i in range(10):
    #     User(username=f'username{random.randint(a=100, b=1000)}',name=f'name{i}', surname=f'surname{i}', email=f'mail{random.randint(a=100, b=1000)}@mail.ru', password=f'password{i}').save()
    User.get_user_choices()
    context = {'TaskForm': TaskForm(), 'UserForm': UserForm(), 'FileForm': FileFieldForm()}
    return render(request, 'index.html', context=context)
