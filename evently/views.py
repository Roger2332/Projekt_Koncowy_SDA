from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.http import HttpResponse, JsonResponse

from .forms import CreateEventForm, CreateUserForm, CategoryForm, EventSearchForm, CommentForm
from .models import Category, Event, CreateUserModel, Status, Comment


@login_required  # Dekorator Sprawdza czy uzytkownik jest zalogowany, jesli nie jest zostanie przekierowany na strone do logowania
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(
            request.POST)  # Inicjalizacja formularza CreateEventForm z danymi przekazanymi z żądania POST
        if form.is_valid():  # Sprawdzenie poprawności danych formularza
            event = form.save(commit=False)
            form.instance.author = request.user  # Przypisanie bieżącego użytkownika jako autora wydarzenia
            form.save()  # Zapisanie formularza do bazy danych
            return redirect('detail_event', pk=event.pk)  # Przekierowanie na stronę szczegółów utworzonego wydarzenia
    else:
        form = CreateEventForm()  # Utworzenie pustego formularza CreateEventForm w przypadku, gdy żądanie nie jest metodą POST
    return render(request, 'create_event.html', {
        'form': form})  # Renderowanie szablonu create_event.html z przekazaniem formularza do kontekstu szablonu


# Widok umozliwiajacy tworzenie uzytkownikow
class UserCreateView(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    # Przekierowanie po stworzeniu uzytkownika
    success_url = reverse_lazy('list_events')


# Widok umozliwiajacy tworzenie Kategori
class CreateCategoryView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('create_category'),
    # Sprawdzanie czy uzytkownik jest superuser(Administratorem)
    permission_required = 'is_superuser'


# Widok tworzacy liste eventów
def list_events(request, form=None):
    #new
    if request.user.is_authenticated and request.user.is_superuser:
        events = Event.objects.all().order_by('start_at')
    else:
        events = Event.objects.filter(status=1).order_by('start_at')
    return render(request, 'event_list.html', {
        'events': events,
        'form': form,
        'is_admin': request.user.is_authenticated and request.user.is_superuser
    })


# Widok strony głównej
def homepage(request):
    return render(request, 'homepage.html')


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
        # Pobieranie aktualnego czasu
        now = datetime.now().date()
        # W zależności od wybranego typu wyszukiwania, filtrowanie wydarzeń
        if search_type:
            # Wydarzenia przyszłe
            if search_type == 'future':
                events = events.filter(start_at__gt=now)
            # Wydarzenia przeszłe
            elif search_type == 'past':
                events = events.filter(end_at__lt=now)
            # Wydarzenia trwające i przyszłe
            elif search_type == 'ongoing_future':
                events = events.filter(end_at__gt=now)
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
    return redirect('detail_event', pk=event.id)


# Wyrejestrowanie sie do eventu
def unsubscribe_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    # Sprawdzenie, czy użytkownik jest uczestnikiem wydarzenia
    if not event.participants.filter(id=request.user.id).exists():
        return HttpResponse('Nie jesteś zarejestrowany na to wydarzenie.', status=400)
    # Usunięcie użytkownika z uczestników wydarzenia
    event.participants.remove(request.user)
    # Przekierowanie do szczegółów wydarzenia po rezygnacji
    return redirect('detail_event', pk=event.id)


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
            if form.is_valid():
                # Pobranie danych z formularza po poprawnej walidacji
                event = form.save(commit=False)  # Zapisanie formularza, ale bez zapisywania w bazie danych
                # Ustawienie statusu na "Inactive"
                event.status = Status.objects.get(name='Inactive')
                # Zapisanie wydarzenia z ustawionym statusem
                event.save()
                return redirect('detail_event', pk=event.id)  # Po edycji przekierowanie do szczegółów wydarzenia
        else:
            # Tworzenie formularza z istniejącą instancją wydarzenia
            form = CreateEventForm(instance=event)
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'form.html', {'form': form, 'event': event})
    # Odpowiedź HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia
    return HttpResponse('Nie jesteś organizatorem', status=403)


# Widok usuwania wydarzenia
@login_required
def delete_event(request, pk):
    # Pobranie wydarzenia na podstawie id
    event = get_object_or_404(Event, id=pk)
    # Sprawdzenie, czy użytkownik jest autorem wydarzenia
    if request.user == event.author:
        if request.method == 'POST':
            event.delete()
            # Po usunieciu przekierowanie do szczegółów wydarzenia
            return redirect('list_events')
        # Renderowanie formularza, zarówno w przypadku GET jak i błędów walidacji
        return render(request, 'delete_event.html', {'event': event})
    # Zwrócenie odpowiedzi HTTP 403, jeśli użytkownik nie jest uprawniony do edycji wydarzenia
    return HttpResponse('Nie jesteś organizatorem', status=403)


# Widok calego wydarzenia
def detail_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = Comment.objects.filter(event=event).order_by('added')
    # Sprawdzanie czy zalogowany uzytkownik to autor wydarzenia
    is_organizer = request.user == event.author
    # Sprawdzenie, czy użytkownik jest zarejestrowany na wydarzenie
    is_registered = event.participants.filter(id=request.user.id).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            # Tworzenie komentarza z danych formularza, bez zapisywania do bazy danych (commit=False).
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.event = event
                comment.save()
                return redirect('detail_event', pk=event.pk)
        # Jeżeli użytkownik nie zostanie uwierzytelniony,
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'detail_event.html', {
        # Przekazanie obiektu wydarzenia do szablonu
        'event': event,
        'comments': comments,
        # Informacja czy zalogowany użytkownik jest organizatorem wydarzenia Boolen True lub False
        'is_organizer': is_organizer,
        # Informacja czy zalogowany użytkownik jest zarejestrowany na wydarzenie
        'is_registered': is_registered,
        'form': form,
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

# wykonaj zapytanie do bazy danych, aby uzyskać wszystkie obiekty Event, w których bieżący użytkownik znajduje się na liście uczestników.
@login_required
def user_subscriptions(request, pk):
    user = request.user
    subscribed_events = Event.objects.filter(participants=user)
    return render(request, 'user_subscriptions.html', {'subscribed_events': subscribed_events})


def user_is_admin(user):
    return user.is_authenticated and user.is_superuser


# Dekorator csrf_exempt pozwala na wyłączenie wymogu przesyłania tokena CSRF dla tego widoku.
@csrf_exempt
@user_passes_test(user_is_admin)
def update_event_status(request):
    if request.method == 'POST':
        # Pobierz ID wydarzenia z danych POST
        event_id = request.POST.get('event_id')
        # Pobierz nazwę nowego statusu z danych POST
        new_status_name = request.POST.get('new_status')

        try:
            # Spróbuj pobrać wydarzenie o danym ID
            event = Event.objects.get(id=event_id)
            # Spróbuj pobrać nowy status po nazwie
            new_status = Status.objects.get(name=new_status_name)
            # Przypisz nowy status do wydarzenia
            event.status = new_status
            # Zapisz zmiany w bazie danych
            event.save()
            # Zwróć odpowiedź JSON o sukcesie
            return JsonResponse({'success': True})

        # Obsłuż brak wydarzenia
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})

        # Obsłuż brak statusu
        except Status.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Status not found'})

    # Obsłuż nieprawidłowy typ żądania
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@user_passes_test(user_is_admin)
def admin_status_view(request):
    # Utwórz formularz do wyszukiwania wydarzeń na podstawie danych GET
    form = EventSearchForm(request.GET)
    # Pobierz wydarzenia o statusie "Inactive" i posortowane według daty modyfikacji
    events = Event.objects.filter(status__name='Inactive').order_by('modified')

    # Zwróć renderowanie szablonu HTML 'event_status_admin_list.html' z przekazaniem wydarzeń i formularza do kontekstu
    return render(request, 'event_status_admin_list.html', {'events': events, 'form': form})



def Linkedlin_Roger(request):
    response = redirect('https://www.linkedin.com/in/rogerszwaja')
    return response


def Linkedlin_Artema(request):
    response = redirect('https://www.linkedin.com/in/artem-monkiewicz')
    return response
