from django.contrib.auth.forms import UserCreationForm

from .models import CreateUserModel


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email',]



