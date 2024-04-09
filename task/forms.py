from django import forms


class TaskForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    deadline = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    priority = forms.CharField(widget=forms.Select(choices=[]))
    executors = forms.CharField(widget=forms.Select(choices=[]))
    file = forms.FileField(widget=forms.FileInput())
