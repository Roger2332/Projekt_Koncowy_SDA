from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q

from .forms import EventForm, CreateUserForm, CategoryForm, SubscriptionForm, EventSearchForm

from .models import Status, Category, Event


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
def subscribe_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('event_detail', event_id=event_id)
            except forms.ValidationError as e:
                form.add_error(None, e)
    else:
        form = SubscriptionForm(initial={'user': request.user, 'event': event})
    return render(request, 'subscribe_event.html', {'form': form, 'event': event})

#new

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

    return render(request, 'search_results_list.html', {'form': form, 'events': events})



def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})