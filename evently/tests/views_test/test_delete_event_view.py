import pytest
from django.urls import reverse
from django.test import Client
from evently.models import Event, Status, CreateUserModel


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return CreateUserModel.objects.create_user(username='testuser', email='user@example.com', password='12345')


@pytest.fixture
def author():
    return CreateUserModel.objects.create_user(username='author', email='author@example.com', password='12345')


@pytest.fixture
def sample_status():
    status1 = Status.objects.create(name='Active')
    return status1


@pytest.fixture
def event(author, sample_status):
    return Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at='2024-07-01',
        end_at='2024-07-02',
        description='Opis wydarzenia',
        status=sample_status,
        author=author)


@pytest.mark.django_db
def test_delate_event_logged_in_author(client, user, author, event):
    # Logujemy się jako autor wydarzenia
    client.force_login(author)

    # Wysyłamy żądanie GET do edycji wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))

    # Sprawdzamy, czy status odpowiedzi HTTP jest równy 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_event_logged_in_not_author(client, user, event):
    # Logujemy się jako zwykły użytkownik
    client.force_login(user)

    # Wysyłamy żądanie GET do edycji wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))

    # Sprawdzamy, czy status odpowiedzi HTTP jest równy 403 (brak uprawnień)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_event_not_logged_in(client, event):
    # Wysyłamy żądanie GET do delate wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))

    # Sprawdzamy, czy status odpowiedzi HTTP jest równy 302 (przekierowanie do logowania)
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')
