from django.test import Client
from django.urls import reverse
import pytest
from evently.models import CreateUserModel, Status, Event


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
        start_at='2024-07-01',
        end_at='2024-07-02',
        description='Opis wydarzenia',
        status=sample_statuses,
        author=user
    )


@pytest.mark.django_db
def test_subscribe_event_view_with_authenticated_user(client, user, event):
    client.force_login(user)
    url = reverse('subscribe_event', kwargs={'event_id': event.id})
    response = client.get(url)

    assert response.status_code == 302
    assert 'detail_event' in response.url

    assert event.participants.filter(id=user.id).exists()


@pytest.mark.django_db
def test_subscribe_event_view_with_authenticated_user_x2(client, user, event):
    client.force_login(user)
    url = reverse('subscribe_event', kwargs={'event_id': event.id})
    response = client.get(url)

    response2 = client.get(url)

    assert response2.status_code == 400
    assert 'Jesteś już zarejestrowany na to wydarzenie.' in response2.content.decode('utf-8')


@pytest.mark.django_db
def test_subscribe_event_view_with_no_authenticated_user(client, event):
    url = reverse('subscribe_event', kwargs={'event_id': event.id})
    response = client.get(url)

    assert response.status_code == 302
    assert 'accounts/login/' in response.url
