from django import forms
from django.forms import DateInput
from . import models

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()


class CreateTask(forms.ModelForm):

    class Meta():
        model =  models.Task
        fields = ('title', 'description', 'due')

        labels = {
            'due': 'Date (yyyy-mm-dd)'
        }


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
