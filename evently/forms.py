from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .validators import title_validator, data_start_validator, dec_valid
from .models import Event, CreateUserModel, Category, Comment


# Formularz umozliwiajacy tworzenie eventu
class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'place', 'start_at', 'end_at', 'description', 'category']  # wyswietl tabele ktore sa w liscie

    name = forms.CharField(max_length=100, validators=[title_validator])
    place = forms.CharField(max_length=100, validators=[title_validator])
    start_at = forms.DateField(widget=forms.SelectDateWidget, validators=[data_start_validator])
    end_at = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea, validators=[dec_valid])
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    def clean(self):
        # Pobranie zwalidowanych danych z klasy nadrzędnej
        cleaned_data = super().clean()

        # Pobranie wartości pól start_at i end_at
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")

        # Walidacja dat: sprawdzenie, czy data end_at jest późniejsza niż start_at
        if start_at and end_at:
            if end_at <= start_at:
                raise ValidationError('The end date must be later than the start date')
        return cleaned_data  # Zwrócenie zwalidowanych danych


# Forma do tworzenia usera
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CreateUserModel
        fields = ['first_name', 'last_name', 'username', 'email', ]


# Forma do tworzenia kategorii
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


# Wyszukiwarka wydarzen
class EventSearchForm(forms.Form):
    # Lista wyborów dla pola search_type
    SEARCH_CHOICES = [
        ('future', 'Future events'),
        ('past', 'Past events'),
        ('ongoing_future', 'Ongoing and future events'),
        ('all', 'All events')
    ]
    # Pole do wyszukiwania po nazwie wydarzenia
    query = forms.CharField(label='Event name', max_length=100, required=False)
    # Pole do wyboru typu wyszukiwania
    search_type = forms.ChoiceField(label='Search type', choices=SEARCH_CHOICES, required=False)
    # Pole do wyszukiwania po nazwie miejsca
    place = forms.CharField(label='Place name', max_length=100, required=False)
    # Pole do wyboru kategorii z modelu Category
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', required=False)
    # Pole do wyboru organizatora z modelu CreateUserModel
    organizer = forms.ModelChoiceField(queryset=CreateUserModel.objects.all(), label='Organizer', required=False)
    # Pole do wprowadzania daty rozpoczęcia
    start_date = forms.DateField(label='Start date', required=False,
                                 widget=forms.TextInput(attrs={'type': 'date'}))
    # Pole do wprowadzania daty zakończenia
    end_date = forms.DateField(label='End date', required=False,
                               widget=forms.TextInput(attrs={'type': 'date'}))


# Forma dla komentarzy
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        # Pole do mozliwosci wpisania komentarza
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }
