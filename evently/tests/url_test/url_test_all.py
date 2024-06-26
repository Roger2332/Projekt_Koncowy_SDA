import pytest
from django.urls import reverse

from django.test import Client
from django.utils import timezone
from datetime import timedelta, date

from evently.models import CreateUserModel, Event, Category, Status


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    users = CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')
    return users



@pytest.fixture
def sample_categories():
    # Tworzenie przykładowych obiektów Category do testów
    category1 = Category.objects.create(name='Kategoria 1')
    category2 = Category.objects.create(name='Kategoria 2')
    return [category1, category2]


@pytest.fixture
def sample_statuses():
    status1 = Status.objects.create(name='Active')
    status2 = Status.objects.create(name='Inactive')
    return (status1, status2)
@pytest.fixture
def sample_events(user, sample_statuses):
    # Tworzenie przykładowych obiektów Event do testów
    event1 = Event.objects.create(name='Wydarzenie 1', place='Miejsce A', start_at=date(2024, 7, 1),
                                  end_at=date(2024, 7, 2), author=user, status_id=sample_statuses[0].id)
    return event1



@pytest.mark.django_db
def test_admin_url(client):
    response = client.get('/admin')
    assert response.status_code == 301


@pytest.mark.django_db
def test_create_category_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('create_category'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_accept_status_url(client):
    response = client.get(reverse('accept_status'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_event_status_url(client):
    response = client.get(reverse('update_event_status'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_homepage_url(client):
    response = client.get(reverse('homepage'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_events_url(client):
    response = client.get(reverse('list_events'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_event_url(client):
    response = client.get(reverse('search_event'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_event_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('create_event'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_event_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('event_edit', args=[sample_events.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_event_authenticated_author(client, user, sample_events):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 200  # Użytkownik jest autorem, więc otrzymujemy dostęp do formularza usuwania

    # Usunięcie wydarzenia
    response = client.post(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 302  # Przekierowanie po usunięciu
    assert not Event.objects.filter(pk=sample_events.pk).exists()  # Sprawdzenie, że wydarzenie zostało usunięte

@pytest.mark.django_db
def test_delete_event_authenticated_not_author(client, user, sample_events):
    # Inny użytkownik (nie autor) próbuje usunąć wydarzenie
    CreateUserModel.objects.create_user(username='otheruser', email='otheruser@example.com', password='54321')
    client.login(username='otheruser', password='54321')
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 403  # Użytkownik nie jest autorem, więc otrzymujemy Forbidden

@pytest.mark.django_db
def test_delete_event_not_authenticated(client, sample_events):
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 302  # Użytkownik nie jest zalogowany, więc otrzymujemy Forbidden


@pytest.mark.django_db
def test_detail_event_url(client, sample_events):
    response = client.get(reverse('detail_event', args=[sample_events.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_subscribe_event_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    csrf_token = login_response.cookies['csrftoken'].value
    response = client.post(reverse('subscribe_event', args=[sample_events.pk]), {'csrfmiddlewaretoken': csrf_token})
    assert response.status_code == 302

    assert response.url == reverse('detail_event', args=[sample_events.pk])


@pytest.mark.django_db
def test_unsubscribe_event_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    csrf_token = login_response.cookies['csrftoken'].value
    response = client.post(reverse('subscribe_event', args=[sample_events.pk]), {'csrfmiddlewaretoken': csrf_token})
    assert response.status_code == 302

    assert response.url == reverse('detail_event', args=[sample_events.pk])


@pytest.mark.django_db
def test_user_create_url(client):
    response = client.get(reverse('user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_url(client):
    response = client.post(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username='testuser', password='12345')
    response = client.post(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')  # sprawdzenie przekierowania

    # Sprawdzenie, czy użytkownik został wylogowany
    response = client.get(reverse('user_profile'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_profile'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_events_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_events', args=[sample_events.pk]))
    assert response.status_code == 302
    assert response.url == reverse('search_event') + '?query=&search_type=all&place=&category=&organizer=1&start_date=&end_date='


@pytest.mark.django_db
def test_user_subscriptions_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_subscriptions', args=[user.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_change_url(client):
    response = client.get(reverse('password_change'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_change_done_url(client):
    response = client.get(reverse('password_change_done'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_reset_url(client):
    response = client.get(reverse('password_reset'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset_done_url(client):
    response = client.get(reverse('password_reset_done'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset_confirm_url(client):
    response = client.get(reverse('password_reset_confirm', args=['uidb64', 'token']))
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset_complete_url(client):
    response = client.get(reverse('password_reset_complete'))
    assert response.status_code == 200
