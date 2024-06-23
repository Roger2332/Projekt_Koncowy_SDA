from concurrent.futures._base import LOGGER
from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponse
from .forms import EventForm, CreateUserForm, CategoryForm, SubscriptionForm, EventSearchForm

from .models import Status, Category, Event, Subscription, CreateUserModel


# Dekorator Sprawdza czy uzytkownik jest zalogowany, jesli nie jest zostanie przekierowany na strone do logowania
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Przypisanie aktualnie zalogowanego użytkownika jako właściciela wydarzenia
            event = form.save(commit=False)
            form.instance.author = request.user
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


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


# Widok tworzacy liste eventów
def list_events(request):
    events = Event.objects.all().order_by('start_at')
    return render(request, 'event_list.html', {'events': events})


# Wyszukiwarka eventów
def search_event(request):
    form = EventSearchForm(request.GET)
    events = Event.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        search_type = form.cleaned_data.get('search_type')
        place = form.cleaned_data.get('place')
        category = form.cleaned_data.get('category')
        organizer = form.cleaned_data.get('organizer')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if query:
            events = events.filter(name__icontains=query)

        now = datetime.now().date()

        if search_type:
            if search_type == 'future':
                events = events.filter(start_at__gt=now)
            elif search_type == 'past':
                events = events.filter(end_at__lt=now)
            elif search_type == 'ongoing_future':
                events = events.filter(end_at__gt=now)

        if place:
            events = events.filter(place__icontains=place)

        if category:
            events = events.filter(category=category)

        if start_date:
            events = events.filter(start_at__gte=start_date)

        if end_date:
            events = events.filter(end_at__lte=end_date)

        if organizer:
            events = events.filter(author=organizer)

    return render(request, 'event_list.html', {'form': form, 'events': events})


# Zapisywanie się do eventów
@login_required
def subscribe_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Sprawdzenie, czy użytkownik jest już uczestnikiem wydarzenia
    if event.participants.filter(id=request.user.id).exists():
        return HttpResponse('Jesteś już zarejestrowany na to wydarzenie.', status=400)

    # Dodanie użytkownika do uczestników wydarzenia
    event.participants.add(request.user)

    # Przekierowanie do szczegółów wydarzenia po zapisaniu się
    return redirect('event_detail', pk=event.id)


# Wyrejestrowanie sie do eventu
def unsubscribe_event(request, pk):
    event = get_object_or_404(Event, id=pk)

    # Sprawdzenie, czy użytkownik jest uczestnikiem wydarzenia
    if not event.participants.filter(id=request.user.id).exists():
        return HttpResponse('Nie jesteś zarejestrowany na to wydarzenie.', status=400)

    # Usunięcie użytkownika z uczestników wydarzenia
    event.participants.remove(request.user)

    # Przekierowanie do szczegółów wydarzenia po rezygnacji
    return redirect('event_detail', pk=event.id)


# Widok edycji
@login_required
def edit_event(request, pk):
    # Pobranie wydarzenia na podstawie klucza podstawowego
    event = get_object_or_404(Event, id=pk)

    # Sprawdzenie, czy użytkownik jest autorem wydarzenia lub administratorem
    if request.user == event.author or request.user.is_staff:
        # Tworzenie formularza z danymi POST i istniejącą instancją wydarzenia
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('event_detail', pk=event.id)  # Po edycji przekierowanie do szczegółów wydarzenia
        # Tworzenie formularza z istniejącą instancją wydarzeniaUmożliwia to wypełnienie formularza danymi istniejącego wydarzenia, aby użytkownik mógł je edytować
        else:
            form = EventForm(instance=event)
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'form.html', {'form': form, 'event': event})
    # Zwrócenie odpowiedzi HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia
    return HttpResponse('Nie jesteś organizatorem', status=403)


# Widok usuwania wydarzenia
@login_required
def delete_event(request, pk):
    # Pobranie wydarzenia na podstawie klucza podstawowego
    event = get_object_or_404(Event, id=pk)
    # Sprawdzenie, czy użytkownik jest autorem wydarzenia lub administratorem
    if request.user == event.author or request.user.is_staff:
        if request.method == 'POST':
            event.delete()
            return redirect('list_events')  # Po usunieciu przekierowanie do szczegółów wydarzenia
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'delete_event.html', {'event': event})
    # Zwrócenie odpowiedzi HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia
    return HttpResponse('Nie jesteś organizatorem', status=403)


# Widok profilu użytkownika
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_organizer = request.user == event.author
    is_registered = event.participants.filter(id=request.user.id).exists()
    return render(request, 'event_detail.html', {
        'event': event,
        'is_organizer': is_organizer,
        'is_registered': is_registered,
    })

# Widok profilu Usera
def user_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Widok wydażeń usera(jak jest organizatorem)
def user_events(request, pk):
    user = get_object_or_404(CreateUserModel, pk=pk)
    if request.user == user:
        events = Event.objects.filter(author=user)
        return render(request, 'search_results_list.html', {'events': events})
    else:
        return render(request, 'search_results_list.html', {'events': []})