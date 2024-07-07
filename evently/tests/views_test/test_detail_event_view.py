import pytest
from django.test import Client
from django.urls import reverse
from evently.models import CreateUserModel, Status, Event, Category, Comment
from django.utils import timezone


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
    event = Event.objects.create(
        name='Wydarzenie 1',
        place='Miejsce A',
        start_at= timezone.now().date(),
        end_at= timezone.now().date() + timezone.timedelta(days=1),
        description='Opis wydarzenia',
        status=sample_status,
        author=users[0],
    )
    event.category.set([sample_category])  # Use .set() method for many-to-many field
    return event


@pytest.fixture
def comment(users, event):
    return Comment.objects.create(
        author=users[0],
        event=event,
        content='Test Comment'
    )


# Szczegóły wydarzenia - organizator
@pytest.mark.django_db
def test_full_event_description_organizer(client, users, event):
    client.login(username='testuser1', password='12345')
    response = client.get(reverse('full_event_description', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_organizer' in response.context
    assert response.context['is_organizer'] == True


# Szczegóły wydarzenia - uczestnik
@pytest.mark.django_db
def test_full_event_description_participant(client, users, event):
    client.login(username='testuser2', password='12345')
    event.participants.add(users[1])
    response = client.get(reverse('full_event_description', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_registered' in response.context
    assert response.context['is_registered'] == True


# Szczegóły wydarzenia - osoba nieuczestnicząca
@pytest.mark.django_db
def test_full_event_description_non_participant(client, users, event):
    client.login(username='testuser2', password='12345')
    response = client.get(reverse('full_event_description', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_registered' in response.context
    assert response.context['is_registered'] == False


# zczegóły wydarzenia - niezalogowany użytkownik
@pytest.mark.django_db
def test_full_event_description_unauthenticated(client, event):
    response = client.get(reverse('full_event_description', args=[event.pk]))
    assert response.status_code == 200
    assert 'is_organizer' in response.context
    assert response.context['is_organizer'] == False
    assert response.context['is_registered'] == False


# Dodawanie poprawnego komentarza
@pytest.mark.django_db
def test_post_valid_comment(client, users, event):
    client.login(username='testuser1', password='12345')
    data = {
        'content': 'New Comment'
    }
    response = client.post(reverse('full_event_description', args=[event.pk]), data)
    assert response.status_code == 302  # Expecting a redirect after successful comment post
    assert Comment.objects.filter(event=event, content='New Comment').exists()


# Dodawanie komentarza przez niezalogowanego użytkownika
@pytest.mark.django_db
def test_post_comment_unauthenticated(client, event):
    data = {
        'content': 'New Comment'
    }
    response = client.post(reverse('full_event_description', args=[event.pk]), data)
    assert response.status_code == 302
    assert not Comment.objects.filter(event=event, content='New Comment').exists()
