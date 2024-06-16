from django.forms import ModelForm

from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'place', 'start_at', 'end_at', 'description']
