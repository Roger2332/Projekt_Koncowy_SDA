import pytest
from django.urls import reverse
from django.test import Client
from evently.models import Event, Status, CreateUserModel
from django.utils import timezone


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def users():
    user1 = CreateUserModel.objects.create_user(username='testuser1', email='user1@example.com', password='12345')
    user2 = CreateUserModel.objects.create_user(username='testuser2', email='user2@example.com', password='12345')
    return [user1, user2]


@pytest.fixture
def sample_status():
    return Status.objects.create(name='Active')


@pytest.fixture
def events(users, sample_status):
    event1 = Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at=timezone.now().date(),
        end_at=timezone.now().date() + timezone.timedelta(days=1),
        description='Opis wydarzenia 1',
        status=sample_status,
        author=users[0]
    )
    event2 = Event.objects.create(
        name='Wydarzenie 2',
        place='Miejsce B',
        start_at=timezone.now().date(),
        end_at=timezone.now().date() + timezone.timedelta(days=1),
        description='Opis wydarzenia 2',
        status=sample_status,
        author=users[1]
    )
    return [event1, event2]


#  Sprawdza wyświetlanie subskrypcji użytkownika do wydarzeń po zalogowaniu
@pytest.mark.django_db
def test_user_subscriptions_view(client, users, events):
    user = users[0]
    event1, event2 = events
    # Dodanie użytkownika do uczestników wydarzeń
    event1.participants.add(user)
    event2.participants.add(user)
    # Logowanie użytkownika
    client.login(username='testuser1', password='12345')
    # Wywołanie widoku
    url = reverse('user_subscriptions', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200
    # Sprawdzenie, czy używany jest właściwy szablon
    assert 'user_subscriptions.html' in [t.name for t in response.templates]
    # Sprawdzenie, czy w kontekście znajdują się odpowiednie wydarzenia
    subscribed_events = response.context['subscribed_events']
    assert set(subscribed_events) == {event1, event2}
