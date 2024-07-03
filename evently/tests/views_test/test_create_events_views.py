import pytest
from django.urls import reverse
from django.test import Client
from evently.models import CreateUserModel, Event, Category, Status
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
def sample_category():
    category = Category.objects.create(name='Sport')
    return category


@pytest.mark.django_db
def test_create_event_send_by_logged_in_user(client, user, sample_category, sample_statuses):
    # Sprawdza, czy zalogowany użytkownik może utworzyć nowe wydarzenie poprzez formularz
    client.login(username='testuser', password='12345')
    initial_event_count = Event.objects.count()
    form_data = {
        'name': 'Nowe wydarzenie',
        'place': 'Miejsce A',
        'start_at': timezone.now().date(),
        'end_at': timezone.now().date() + timezone.timedelta(days=1),
        'description': 'Opis nowego wydarzenia',
        'category': sample_category.pk,  # Wybierz pierwszą kategorię
        'status': sample_statuses.id
    }
    response = client.post(reverse('create_event'), form_data)
    assert response.status_code == 302  # Przekierowanie po zapisaniu formularza
    assert Event.objects.count() == initial_event_count + 1  # Sprawdzenie, czy wydarzenie zostało dodane


@pytest.mark.django_db
def test_create_event_entry_by_logged_in_user(client, user):
    # Sprawdza, czy zalogowany użytkownik ma dostęp do widoku create_event
    client.login(username='testuser', password='12345')
    response = client.get(reverse('create_event'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_event_entry_by_an_unlogged_user(client):
    response = client.get(reverse('create_event'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url
