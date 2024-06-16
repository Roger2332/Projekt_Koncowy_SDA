from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Event, CreateUserModel


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'place', 'start_at', 'end_at', 'description', ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email', ]
