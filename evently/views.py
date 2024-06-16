from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EventForm
# Create your views here.

class EventView(CreateView):
    template_name = 'form.html'
    form_class = EventForm
    success_url = reverse_lazy('hello')