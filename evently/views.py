from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q
from django.http import HttpResponse
from .forms import EventForm, CreateUserForm, CategoryForm, SubscriptionForm, EventSearchForm

from .models import Status, Category, Event, Subscription


@login_required  # Dekorator Sprawedza czy uzytkownik jest zalogowany, jesli nie jest zostanie przekierowany na strone do logowania
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Przypisz aktualnie zalogowanego użytkownika jako właściciela wydarzenia
            form.instance.author = request.user

            form.save()
            return redirect('list_events')
    else:
        form = EventForm()
    return render(request, 'form.html', {'form': form})


# Widok umozliwiajacy tworzenie uzytkownikow
class UserCreationView(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('list_events')


# Widok umozliwiajacy tworzenie Kategori
class CreateCategoryView(CreateView):
    template_name = 'form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('list_events')


# Widok tworzacy liste Eventow
def list_events(request):
    events = Event.objects.all().order_by('start_at')
    return render(request, 'event_list.html', {'events': events})


@login_required
def search_event(request):
    form = EventSearchForm(request.GET)
    events = Event.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        search_type = form.cleaned_data.get('search_type')

        if query:
            events = events.filter(name__icontains=query)

        now = datetime.now().date()

        if search_type == 'future':
            events = events.filter(start_at__gt=now)
        elif search_type == 'ongoing_future':
            events = events.filter(Q(start_at__lte=now, end_at__gte=now) | Q(start_at__gt=now))

    return render(request, 'event_list.html', {'form': form, 'events': events})


@login_required
def subscribe_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == 'POST':
        # Sprawdzenie czy użytkownik nie jest już subskrybowany
        if not Subscription.objects.filter(user=user, event=event).exists():
            Subscription.objects.create(user=user, event=event)
            return HttpResponse("Subscribed successfully.")  # Przekierowanie po subskrypcji
    return HttpResponse("Invalid request method.")  # Przekierowanie w razie błędu
