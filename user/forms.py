from django.forms import ModelForm, PasswordInput
from user.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': PasswordInput()

        }
        fields = ('username', 'email', 'name', 'surname', 'password')
