import pytest
from django.urls import reverse
from django.test import Client
from evently.models import Event, Status, CreateUserModel
from django.utils import timezone


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
        start_at= timezone.now().date(),
        end_at= timezone.now().date() + timezone.timedelta(days=1),
        description='Opis wydarzenia',
        status=sample_status,
        author=author)


# Usuń wydarzenie zalogowanego autora
@pytest.mark.django_db
def test_delate_event_logged_in_author(client, user, author, event):
    client.force_login(author)
    # Wysyłamy żądanie GET do edycji wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))
    assert response.status_code == 200


# Edycja wydarzenia przez zalogowanego użytkownika, który nie jest autorem
@pytest.mark.django_db
def test_edit_event_logged_in_not_author(client, user, event):
    client.force_login(user)
    # Wysyłamy żądanie GET do edycji wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))
    assert response.status_code == 403


# Edycja wydarzenia przez niezalogowanego użytkownika
@pytest.mark.django_db
def test_edit_event_not_logged_in(client, event):
    # Wysyłamy żądanie GET do delate wydarzenia
    response = client.get(reverse('delete_event', kwargs={'pk': event.pk}))
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/')
