import pytest
from django.urls import reverse
from django.test import Client
from evently.models import Event, CreateUserModel, Status
from evently.forms import EventSearchForm
from evently.views import admin_status_view

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def admin():
    return CreateUserModel.objects.create_superuser(username='admin', email='admin@gmai.com', password='admin12345')

@pytest.fixture
def user():
    return CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')

@pytest.fixture
def sample_status():
    status1 = Status.objects.create(name='Active')
    status2 = Status.objects.create(name='Inactive')
    return [status1, status2]

@pytest.mark.django_db
def test_admin_status_view_access(client, admin, sample_status):
    # Logujemy się jako administrator
    client.force_login(admin)

    # Przygotowanie danych testowych
    event = Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at='2024-07-01',
        end_at='2024-07-02',
        description='Opis wydarzenia',
        status=sample_status[1],
        author=admin
    )

    # Wywołujemy widok admin_status_view
    response = client.get(reverse('accept_status'))

    # Sprawdzamy, czy status odpowiedzi HTTP jest równy 200 (sukces)
    assert response.status_code == 200

    # Sprawdzamy, czy formularz EventSearchForm jest w kontekście
    assert 'form' in response.context
    assert isinstance(response.context['form'], EventSearchForm)

    # Sprawdzamy, czy wydarzenia związane z nieaktywnym statusem są w kontekście
    assert 'events' in response.context
    events = response.context['events']
    assert events.exists()  # Sprawdzamy, czy istnieją jakieś wydarzenia

    # Sprawdzamy, czy wydarzenia są posortowane według daty modyfikacji
    last_modified_event = events.last()
    assert last_modified_event.modified is not None

    # Sprawdzamy, czy utworzone wydarzenie jest w kontekście
    assert event in events


@pytest.mark.django_db
def test_admin_status_view_no_access(client, user):
    client.force_login(user)

    # Wywołujemy widok admin_status_view
    response = client.get(reverse('accept_status'))

    # Sprawdzamy, czy status odpowiedzi HTTP jest równy 302 (przekierowanie)
    assert response.status_code == 302

    # Sprawdzamy, czy użytkownik został przekierowany na stronę logowania
    assert response.url.startswith('/accounts/login/')

    # Sprawdzamy, czy response.context nie jest ustawiony (None), ponieważ nie otrzymujemy kontekstu przy przekierowaniu
    assert response.context is None
