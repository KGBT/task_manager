from datetime import datetime, date

from django import forms
from django.forms import ModelForm, Form
from task.models import Priority, Task, File


class TaskForm(ModelForm):
    name = forms.CharField(label='Наименование задачи', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Наименование задачи'}))
    date_end = forms.DateField(label='Выбор даты', required=False,
                               widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker form-control'}),
                               initial=date.today())
    description = forms.CharField(label='Описание (необязательно)', required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Описание (необязательно)', 'style': 'height: 250px;'}))

    class Meta:
        model = Task
        fields = ['name', 'date_end', 'description']

    def __init__(self, user_login, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executors'] = forms.CharField(label='Исполнитель',
                                                   widget=forms.Select(choices=user_login.get_employees_for_choice(),
                                                                       attrs={'class': 'form-select',
                                                                              'aria-label': ''}))


#     name = forms.CharField(label='Name', max_length=50)
#     description = forms.CharField(widget=forms.Textarea, max_length=1000)
#     deadline = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
#     priority = forms.ChoiceField(choices=Priority.PRIORITY_CHOICES)
#     executors = forms.CharField(widget=forms.Select(choices=User.get_user_choices()))


class PriorityForm(ModelForm):
    priority = forms.ChoiceField(label='Приоритет', choices=Priority.PRIORITY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select', 'aria-label': ''}))

    class Meta:
        model = Priority
        fields = ['priority']


class FileForm(ModelForm):
    path = forms.FileField(label='Загрузка', required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}))

    class Meta:
        model = File
        fields = ['path']

# Это не работает
# class FileForm(forms.Form):
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))


# Для загрузки нескольких файлов создаем несколько классов
# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True
#
#
# class MultipleFileField(forms.FileField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("widget", MultipleFileInput())
#         super().__init__(*args, **kwargs)
#
#     def clean(self, data, initial=None):
#         single_file_clean = super().clean
#         if isinstance(data, (list, tuple)):
#             result = [single_file_clean(d, initial) for d in data]
#         else:
#             result = single_file_clean(data, initial)
#         return result
#
#
# class FileFieldForm(forms.Form):
#     file_field = MultipleFileField()
