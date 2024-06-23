from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse

from .forms import CreateEventForm, CreateUserForm, CategoryForm, EventSearchForm
from .models import Category, Event, CreateUserModel


@login_required  # Dekorator Sprawdza czy uzytkownik jest zalogowany, jesli nie jest zostanie przekierowany na strone do logowania
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)  # Inicjalizacja formularza CreateEventForm z danymi przekazanymi z żądania POST
        if form.is_valid():  # Sprawdzenie poprawności danych formularza
            event = form.save(commit=False)
            form.instance.author = request.user  # Przypisanie bieżącego użytkownika jako autora wydarzenia
            form.save()  # Zapisanie formularza do bazy danych
            return redirect('event_detail', pk=event.pk)  # Przekierowanie na stronę szczegółów utworzonego wydarzenia
    else:
        form = CreateEventForm()  # Utworzenie pustego formularza CreateEventForm w przypadku, gdy żądanie nie jest metodą POST
    return render(request, 'create_event.html', {
        'form': form})  # Renderowanie szablonu create_event.html z przekazaniem formularza do kontekstu szablonu


# Widok umozliwiajacy tworzenie uzytkownikow
class UserCreateView(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('list_events')  # Przekierowanie po stworzeniu uzytkownika


# Widok umozliwiajacy tworzenie Kategori
class CreateCategoryView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('create_category'),
    permission_required = 'is_superuser'  # Sprawdzanie czy uzytkownik jest superuser(Administratorem)


# Widok tworzacy liste eventów
def list_events(request):
    form = EventSearchForm(request.GET)
    events = Event.objects.all().order_by('start_at')  # Sortowanie wydarzen po dacie
    return render(request, 'event_list.html', {'events': events, 'form': form})


# Widok strony głównej
def home_views(request):
    return render(request, 'home.html', {'home_views': home_views})


# Wyszukiwarka eventów
def search_event(request):
    # Tworzymy formularz na podstawie danych GET przesłanych przez użytkownika
    form = EventSearchForm(request.GET)

    # Pobieramy wszystkie wydarzenia
    events = Event.objects.all()

    if form.is_valid():
        # Pobieramy dane z formularza
        query = form.cleaned_data.get('query')
        search_type = form.cleaned_data.get('search_type')
        place = form.cleaned_data.get('place')
        category = form.cleaned_data.get('category')
        organizer = form.cleaned_data.get('organizer')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        # Filtrujemy wydarzenia na podstawie nazwy zawierającej podany ciąg znaków
        if query:
            events = events.filter(name__icontains=query)

        now = datetime.now().date()  # Pobieranie aktualnego czasu

        # W zależności od wybranego typu wyszukiwania, filtrowanie wydarzeń
        if search_type:
            if search_type == 'future':
                events = events.filter(start_at__gt=now)  # Wydarzenia przyszłe
            elif search_type == 'past':
                events = events.filter(end_at__lt=now)  # Wydarzenia przeszłe
            elif search_type == 'ongoing_future':
                events = events.filter(end_at__gt=now)  # Wydarzenia trwające i przyszłe

        # Filtrowanie wydarzeń po miejscu (nazwa miejsca zawiera podany ciąg znaków)
        if place:
            events = events.filter(place__icontains=place)

        # Filtrowanie wydarzeń po kategorii
        if category:
            events = events.filter(category=category)

        # Filtrowanie wydarzeń, które rozpoczynają się od podanej daty lub później
        if start_date:
            events = events.filter(start_at__gte=start_date)

        # Filtrowanie wydarzeń, które kończą się do podanej daty lub wcześniej
        if end_date:
            events = events.filter(end_at__lte=end_date)

        # Filtrowanie wydarzeń po autorze (organizatorze)
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
    # Pobranie wydarzenia na podstawie id
    event = get_object_or_404(Event, id=pk)

    # Sprawdzenie, czy użytkownik jest autorem wydarzenia
    if request.user == event.author:
        # Tworzenie formularza z danymi POST i istniejącą wartosciami
        if request.method == 'POST':
            form = CreateEventForm(request.POST, instance=event)
            if form.is_valid():  # Pobieranie danych z formularza po poprawnej walidacji
                form.save()
                return redirect('event_detail', pk=event.id)  # Po edycji przekierowanie do szczegółów wydarzenia

        # Tworzenie formularza z istniejącą instancją wydarzenia Umożliwia to wypełnienie formularza danymi istniejącego wydarzenia, aby użytkownik mógł je edytować
        else:
            form = CreateEventForm(instance=event)
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'form.html', {'form': form, 'event': event})

    return HttpResponse('Nie jesteś organizatorem',
                        status=403)  # Zwrócenie odpowiedzi HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia


# Widok usuwania wydarzenia
@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, id=pk)  # Pobranie wydarzenia na podstawie id
    if request.user == event.author:  # Sprawdzenie, czy użytkownik jest autorem wydarzenia
        if request.method == 'POST':
            event.delete()
            return redirect('list_events')  # Po usunieciu przekierowanie do szczegółów wydarzenia
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'delete_event.html', {'event': event})

    # Zwrócenie odpowiedzi HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia
    return HttpResponse('Nie jesteś organizatorem', status=403)


# Widok calego wydarzenia
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_organizer = request.user == event.author  # Sprawdzanie czy zalogowany uzytkownik to autor wydarzenia
    # Sprawdzenie, czy użytkownik jest zarejestrowany na wydarzenie
    is_registered = event.participants.filter(id=request.user.id).exists()
    return render(request, 'event_detail.html', {
        'event': event,  # Przekazanie obiektu wydarzenia do szablonu
        # Informacja czy zalogowany użytkownik jest organizatorem wydarzenia Boolen True lub False
        'is_organizer': is_organizer,
        # Informacja czy zalogowany użytkownik jest zarejestrowany na wydarzenie
        'is_registered': is_registered,
    })


# Widok profilu Usera
def user_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# Widok wydażeń usera
def user_events(request, pk):
    user = get_object_or_404(CreateUserModel, pk=pk)
    if request.user == user:
        events = Event.objects.filter(author=user)
        return redirect(f'/search/?query=&search_type=all&place=&category=&organizer={user.id}&start_date=&end_date=')
    else:
        return redirect('/search/?query=&search_type=all&place=&category=&organizer=&start_date=&end_date=')


@login_required
def user_subscriptions(request):
    user = request.user
    subscribed_events = Event.objects.filter(participants=user)
    return render(request, 'user_subscriptions.html', {'subscribed_events': subscribed_events})


def Linkedlin_Roger(request):
    response = redirect('https://www.linkedin.com/in/rogerszwaja')
    return response


def Linkedlin_Artema(request):
    response = redirect('https://www.linkedin.com/in/artem-monkiewicz')
    return response
