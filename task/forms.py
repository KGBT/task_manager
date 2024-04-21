# from django import forms
#
# from task.models import Priority
# from user.models import User
#
#
# class TaskForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=50)
#     description = forms.CharField(widget=forms.Textarea, max_length=1000)
#     deadline = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
#     priority = forms.ChoiceField(choices=Priority.PRIORITY_CHOICES)
#     executors = forms.CharField(widget=forms.Select(choices=User.get_user_choices()))
#
# #Это не работает
# class FileForm(forms.Form):
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
#
#
# #Для загрузки нескольких файлов создаем несколько классов
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
