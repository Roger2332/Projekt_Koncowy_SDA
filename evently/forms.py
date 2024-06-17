from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import Event, CreateUserModel, Category, Status, Subscription


# sprawdzanie czy tytul nie zawiera samych bialych znakow
def title_validator(value):
    if value == '' * len(value):
        raise forms.ValidationError('The title cannot contain only trademarks')


# sprawdzanie czy data nie jest wpisana przeszla
def data_start_validator(value):
    if value < datetime.now().date():
        raise forms.ValidationError('The data cannot be in the future')


# ZMIANA -nowy validator
# sprawdzanie czy date_start > date_end
def data_end_validator(date_end):
    def validate(date_start):
        if date_start and date_end:
            if date_start > date_end:
                raise forms.ValidationError('The end date cannot be earlier than the start date')

    return validate


# Sprawdzanie czy tresc zawiera conajmniej 20 znakow
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
    end_at = forms.DateField(widget=forms.SelectDateWidget,
                             validators=[data_end_validator])  # ZMIANA zapis nowego validatora!
    description = forms.CharField(widget=forms.Textarea, validators=[dec_valid])
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label="Wybierz kategorię"
                                      )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def save(self,
             commit=True):  # Dodanie statusu nieaktywnego odrazu jak uzytkownik stworzy konto, admin musi mu aktywowac konto
        self.instance.is_active = False
        return super().save(commit)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        unique_together = ('user', 'event')  # sprawdzanie na unikatowość
        fields = ['user', 'event']

    # sprawdzanie, czy user nie podpisuje się na własny event
    def clean(self):
        if self.user == self.event.author:
            raise ValidationError("You cannot sign up for your own event.")
        # sprawdzanie, czy user nie jest już podpisany na event
        if Subscription.objects.filter(user=self.user, event=self.event).exists():
            raise ValidationError("You are already subscribed to this event.")
