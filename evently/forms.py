from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Event, CreateUserModel, Category


def title_validator(value):
    if value == '' * len(value):
        raise forms.ValidationError('The title cannot contain only trademarks')


def data_start_validator(value):
    if value < datetime.now().date():
        raise forms.ValidationError('The data cannot be in the future')


# def data_end_validator(date_start, date_end):
#     if date_start > date_end:
#         raise forms.ValidationError('The end date cannot be greater than the start date')


def dec_valid(value):
    if len(value) < 20:
        raise forms.ValidationError('Description must contain at least 20 characters')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'place', 'start_at', 'end_at', 'description', 'category']

    name = forms.CharField(max_length=100, validators=[title_validator])
    place = forms.CharField(max_length=100, validators=[title_validator])
    start_at = forms.DateField(widget=forms.SelectDateWidget, validators=[data_start_validator])
    end_at = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea, validators=[dec_valid])
    category = forms.ChoiceField(choices=Category.CATEGORY_CHOICES)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit)

# Roger Comment

# comment

# Roger Comment