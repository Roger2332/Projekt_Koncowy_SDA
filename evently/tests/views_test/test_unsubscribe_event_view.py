from django.test import Client
from django.urls import reverse
import pytest
from evently.models import CreateUserModel, Status, Event
from django.utils import timezone


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    users = CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')
    return users


@pytest.fixture
def sample_statuses():
    status1 = Status.objects.create(name='Active')
    return status1


@pytest.fixture
def event(user, sample_statuses):
    return Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at=timezone.now().date(),
        end_at=timezone.now().date() + timezone.timedelta(days=1),
        description='Opis wydarzenia',
        status=sample_statuses,
        author=user
    )


# Odsubskrypcja wydarzenia przez użytkownika, który nie jest zarejestrowany na wydarzenie
@pytest.mark.django_db
def test_unsubscribe_event_not_registered(client, user, event):
    client.force_login(user)
    # Wywołujemy widok unsubscribe_event dla użytkownika niezarejestrowanego na wydarzenie
    url = reverse('unsubscribe_event', kwargs={'pk': event.id})
    response = client.get(url)
    # Sprawdzamy, czy odpowiedź zawiera oczekiwany komunikat
    assert response.status_code == 400
    assert 'Nie jesteś zarejestrowany na to wydarzenie.' in response.content.decode('utf-8')


# Odsubskrypcja wydarzenia przez użytkownika, który jest zarejestrowany na wydarzenie
@pytest.mark.django_db
def test_unsubscribe_event_registered(client, user, event):
    client.force_login(user)
    # Dodajemy użytkownika jako uczestnika wydarzenia
    event.participants.add(user)
    url = reverse('unsubscribe_event', kwargs={'pk': event.id})
    response = client.get(url, follow=True)
    # Sprawdzamy, czy użytkownik został usunięty z listy uczestników wydarzenia
    assert not event.participants.filter(id=user.id).exists()
    assert response.status_code == 200


# Próba odsubskrypcji wydarzenia przez niezalogowanego użytkownika
@pytest.mark.django_db
def test_unsubscribe_event_unauthenticated(client, event):
    url = reverse('unsubscribe_event', kwargs={'pk': event.id})
    response = client.get(url)
    assert reverse('login')
