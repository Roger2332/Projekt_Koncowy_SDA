import pytest
from django.test import Client
from django.urls import reverse
from evently.models import CreateUserModel, Status, Event, Category, Comment

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def users():
    user1 = CreateUserModel.objects.create_user(username='testuser1', email='user1@gmail.com', password='12345')
    user2 = CreateUserModel.objects.create_user(username='testuser2', email='user2@gmail.com', password='12345')
    return user1, user2

@pytest.fixture
def sample_status():
    return Status.objects.create(name='Active')

@pytest.fixture
def sample_category():
    return Category.objects.create(name='Category 1')

@pytest.fixture
def event(users, sample_status, sample_category):
    return Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at='2024-07-01',
        end_at='2024-07-02',
        description='Opis wydarzenia',
        status=sample_status,
        author=users[0],
        category=sample_category
    )

@pytest.fixture
def comment(users, event):
    return Comment.objects.create(
        author=users[0],
        event=event,
        content='Test Comment'
    )

@pytest.mark.django_db
def test_detail_event_organizer(client, users, event):
    client.login(username='testuser1', password='12345')
    response = client.get(reverse('detail_event', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_organizer' in response.context
    assert response.context['is_organizer'] == True

@pytest.mark.django_db
def test_detail_event_participant(client, users, event):
    client.login(username='testuser2', password='12345')
    event.participants.add(users[1])
    response = client.get(reverse('detail_event', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_registered' in response.context
    assert response.context['is_registered'] == True

@pytest.mark.django_db
def test_detail_event_non_participant(client, users, event):
    client.login(username='testuser2', password='12345')
    response = client.get(reverse('detail_event', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_registered' in response.context
    assert response.context['is_registered'] == False

@pytest.mark.django_db
def test_detail_event_unauthenticated(client, event):
    response = client.get(reverse('detail_event', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_organizer' in response.context
    assert response.context['is_organizer'] == False
    assert response.context['is_registered'] == False

@pytest.mark.django_db
def test_post_valid_comment(client, users, event):
    client.login(username='testuser1', password='12345')
    data = {
        'content': 'New Comment'
    }
    response = client.post(reverse('detail_event', args=[event.pk]), data)
    assert response.status_code == 302  # Expecting a redirect after successful comment post
    assert Comment.objects.filter(event=event, content='New Comment').exists()

@pytest.mark.django_db
def test_post_comment_unauthenticated(client, event):
    data = {
        'content': 'New Comment'
    }
    response = client.post(reverse('detail_event', args=[event.pk]), data)
    assert response.status_code == 302
    assert not Comment.objects.filter(event=event, content='New Comment').exists()
