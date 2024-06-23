from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import Event, CreateUserModel, Category


# Sprawdzanie czy tytul nie zawiera samych bialych znakow
def title_validator(value):
    if value == '' * len(value):
        raise forms.ValidationError('The title cannot contain only trademarks')


# Sprawdzanie czy data nie jest wpisana przeszla
def data_start_validator(value):
    if value < datetime.now().date():
        raise forms.ValidationError('The date cannot be past')


# Sprawdzanie czy tresc zawiera conajmniej 20 znakow
def dec_valid(value):
    if len(value) < 20:
        raise forms.ValidationError('Description must contain at least 20 characters')


# Formularz umozliwiajacy tworzenie eventu
class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event  # sciagniecie modelu eventu
        fields = ['name', 'place', 'start_at', 'end_at', 'description', 'category']  # wyswietl tabele ktore sa w liscie

    name = forms.CharField(max_length=100, validators=[title_validator])
    place = forms.CharField(max_length=100, validators=[title_validator])
    start_at = forms.DateField(widget=forms.SelectDateWidget, validators=[data_start_validator])
    end_at = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea, validators=[dec_valid])
    category = forms.ModelChoiceField(queryset=Category.objects.all(),  # do poprawy
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      empty_label="Wybierz kategorię"
                                      )

    def clean(self):
        # Pobranie zwalidowanych danych z klasy nadrzędnej
        cleaned_data = super().clean()

        # Pobranie wartości pól start_at i end_at
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")

        # Walidacja dat: sprawdzenie, czy data end_at jest późniejsza niż start_at
        if start_at and end_at:
            if end_at <= start_at:
                raise ValidationError('Data zakończenia musi być późniejsza niż data rozpoczęcia')
        return cleaned_data  # Zwrócenie zwalidowanych danych

    def __init__(self, *args, **kwargs):
        # Inicjalizacja formularza za pomocą danych przekazanych jako argumenty
        super().__init__(*args, **kwargs)


# Forma do tworzenia usera
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def save(self, commit=True):
        return super().save(commit)


# Forma do tworzenia kategorii
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


# Wyszukiwarka wydarzen
class EventSearchForm(forms.Form):
    # Lista wyborów dla pola search_type
    SEARCH_CHOICES = [
        ('future', 'Przyszłe'),
        ('past', 'Przeszłe'),
        ('ongoing_future', 'Trwające i przyszłe'),
        ('all', 'Wszystkie')
    ]
    # Pole do wyszukiwania po nazwie wydarzenia
    query = forms.CharField(label='Nazwa wydarzenia', max_length=100, required=False)
    # Pole do wyboru typu wyszukiwania
    search_type = forms.ChoiceField(label='Typ wyszukiwania', choices=SEARCH_CHOICES, required=False)
    # Pole do wyszukiwania po nazwie miejsca
    place = forms.CharField(label='Nazwa miejsca', max_length=100, required=False)
    # Pole do wyboru kategorii z modelu Category
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Kategoria', required=False)
    # Pole do wyboru organizatora z modelu CreateUserModel
    organizer = forms.ModelChoiceField(queryset=CreateUserModel.objects.all(), label='Organizator', required=False)
    # Pole do wprowadzania daty rozpoczęcia
    start_date = forms.DateField(label='Data rozpoczęcia', required=False,
                                 widget=forms.TextInput(attrs={'type': 'date'}))
    # Pole do wprowadzania daty zakończenia
    end_date = forms.DateField(label='Data zakończenia', required=False,
                               widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamiczne ustawienie queryset dla pola place na podstawie unikalnych miejsc z obiektów Event
        self.fields['place'].queryset = Event.objects.values_list('place', flat=True).distinct()
