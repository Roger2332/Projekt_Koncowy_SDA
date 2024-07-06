import pytest
from django.urls import reverse

from django.test import Client

from datetime import date

from evently.models import CreateUserModel, Event, Status


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin():
    return CreateUserModel.objects.create_superuser(username='admin', email='admin@gmai.com', password='admin12345')


@pytest.fixture
def user():
    users = CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')
    return users


@pytest.fixture
def sample_statuses():
    status1 = Status.objects.create(name='Active')
    return status1


# Tworzenie przykładowych obiektów Event do testów
@pytest.fixture
def sample_events(user, sample_statuses):
    event1 = Event.objects.create(name='Wydarzenie 1', place='Miejsce A', start_at=date(2024, 7, 1),
                                  end_at=date(2024, 7, 2), author=user, status_id=sample_statuses.id)
    return event1


# Dostęp admina do panelu admina
@pytest.mark.django_db
def test_admin_url_by_the_admin(client, admin):
    logged_in = client.login(username='admin', password='admin12345')
    assert logged_in
    response = client.get('/admin/')
    assert response.status_code == 200


# Brak dostępu użytkownika do panelu admina
@pytest.mark.django_db
def test_admin_url_by_the_user(client, user):
    logged_in = client.login(username='testuser', password='12345')
    assert logged_in
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/admin/login/' in response.url


# Brak dostępu użytkownika do tworzenia kategorii
@pytest.mark.django_db
def test_create_category_url_by_the_user(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('create_category'))
    assert response.status_code == 403


# Dostęp admina do tworzenia kategorii
@pytest.mark.django_db
def test_create_category_url_by_the_admin(client, admin):
    client.login(username='admin', password='admin12345')
    response = client.get(reverse('create_category'))
    assert response.status_code == 200


# Brak dostępu niezalogowanego użytkownika do akceptacji statusu
@pytest.mark.django_db
def test_accept_status_url_no_user(client):
    response = client.get(reverse('accept_status'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Brak dostępu zalogowanego użytkownika do akceptacji statusu
@pytest.mark.django_db
def test_accept_status_url_by_the_user(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('accept_status'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Dostęp admina do akceptacji statusu
@pytest.mark.django_db
def test_accept_status_url_by_the_admin(client, admin):
    client.login(username='admin', password='admin12345')
    response = client.get(reverse('accept_status'))
    assert response.status_code == 200


# Brak dostępu niezalogowanego użytkownika do aktualizacji statusu wydarzenia
@pytest.mark.django_db
def test_update_event_status_url_no_user(client):
    response = client.get(reverse('update_event_status'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Brak dostępu zalogowanego użytkownika do aktualizacji statusu wydarzenia
@pytest.mark.django_db
def test_update_event_status_url_by_the_user(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('update_event_status'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Dostępność strony głównej
@pytest.mark.django_db
def test_homepage_url(client):
    response = client.get(reverse('homepage'))
    assert response.status_code == 200


# Dostępność listy wydarzeń
@pytest.mark.django_db
def test_list_events_url(client):
    response = client.get(reverse('list_events'))
    assert response.status_code == 200


# Dostępność wyszukiwania wydarzeń
@pytest.mark.django_db
def test_search_event_url(client):
    response = client.get(reverse('search_event'))
    assert response.status_code == 200


# Dostęp użytkownika do tworzenia wydarzenia
@pytest.mark.django_db
def test_create_event_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('create_event'))
    assert response.status_code == 200


# Dostęp użytkownika do edycji wydarzenia
@pytest.mark.django_db
def test_edit_event_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('event_edit', args=[sample_events.pk]))
    assert response.status_code == 200


# Usuwanie wydarzenia przez autora
@pytest.mark.django_db
def test_delete_event_authenticated_author(client, user, sample_events):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 200  # Użytkownik jest autorem, więc otrzymujemy dostęp do formularza usuwania
    # Usunięcie wydarzenia
    response = client.post(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 302  # Przekierowanie po usunięciu
    assert 'list_events' in response.url
    assert not Event.objects.filter(pk=sample_events.pk).exists()  # Sprawdzenie, że wydarzenie zostało usunięte


# Inny użytkownik (nie autor) próbuje usunąć wydarzenie
@pytest.mark.django_db
def test_delete_event_authenticated_not_author(client, user, sample_events):
    CreateUserModel.objects.create_user(username='otheruser', email='otheruser@example.com', password='54321')
    client.login(username='otheruser', password='54321')
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 403  # Użytkownik nie jest autorem, więc otrzymujemy Forbidden


# Brak dostępu niezalogowanego użytkownika do usuwania wydarzenia
@pytest.mark.django_db
def test_delete_event_not_authenticated(client, sample_events):
    response = client.get(reverse('delete_event', args=[sample_events.pk]))
    assert response.status_code == 302  # Użytkownik nie jest zalogowany, więc otrzymujemy Forbidden
    assert 'accounts/login' in response.url


# Dostępność szczegółów wydarzenia
@pytest.mark.django_db
def test_detail_event_url(client, sample_events):
    response = client.get(reverse('detail_event', args=[sample_events.pk]))
    assert response.status_code == 200


# Subskrypcja wydarzenia przez użytkownika
@pytest.mark.django_db
def test_subscribe_event_url_by_user(client, sample_events, user):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    csrf_token = login_response.cookies['csrftoken'].value
    response = client.post(reverse('subscribe_event', args=[sample_events.pk]), {'csrfmiddlewaretoken': csrf_token})
    assert response.status_code == 302
    assert response.url == reverse('detail_event', args=[sample_events.pk])


# Brak dostępu niezalogowanego użytkownika do subskrypcji wydarzenia
@pytest.mark.django_db
def test_subscribe_event_url_no_user(client, sample_events):
    response = client.post(reverse('subscribe_event', args=[sample_events.pk]))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Anulowanie subskrypcji wydarzenia przez użytkownika
@pytest.mark.django_db
def test_unsubscribe_event_url(client, sample_events, user):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    csrf_token = login_response.cookies['csrftoken'].value
    response = client.post(reverse('subscribe_event', args=[sample_events.pk]), {'csrfmiddlewaretoken': csrf_token})
    assert response.status_code == 302
    assert response.url == reverse('detail_event', args=[sample_events.pk])


# Dostępność strony użytkownika
@pytest.mark.django_db
def test_user_create_url(client):
    response = client.get(reverse('user'))
    assert response.status_code == 200


# Dostępność strony logowania
@pytest.mark.django_db
def test_login_url(client):
    response = client.post(reverse('login'))
    assert response.status_code == 200

# Wylogowanie użytkownika
@pytest.mark.django_db
def test_logout_view(client, user):
    client.login(username='testuser', password='12345')
    response = client.post(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')  # sprawdzenie przekierowania
    # Sprawdzenie, czy użytkownik został wylogowany
    response = client.get(reverse('user_profile'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Dostępność profilu użytkownika
@pytest.mark.django_db
def test_user_profile_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_profile'))
    assert response.status_code == 200


# Dostępność profilu użytkownika
@pytest.mark.django_db
def test_user_subscriptions_url(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('user_subscriptions', args=[user.pk]))
    assert response.status_code == 200


# Brak dostępu niezalogowanego użytkownika do zmiany hasła
@pytest.mark.django_db
def test_password_change_url_no_user(client):
    response = client.get(reverse('password_change'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Dostępność zmiany hasła użytkownika
@pytest.mark.django_db
def test_password_change_url(client, user):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    response = client.get(reverse('password_change'))
    assert response.status_code == 200


# Brak dostępu niezalogowanego użytkownika do potwierdzenia zmiany hasła
@pytest.mark.django_db
def test_password_change_done_url_no_user(client):
    response = client.get(reverse('password_change_done'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Brak dostępu zalogowanego użytkownika do potwierdzenia zmiany hasła
@pytest.mark.django_db
def test_password_change_done_url_by_user(client):
    client.login(username='testuser', password='12345')
    login_response = client.get(reverse('login'))
    response = client.get(reverse('password_change_done'))
    assert response.status_code == 302
    assert 'accounts/login' in response.url


# Dostępność resetowania hasła
@pytest.mark.django_db
def test_password_reset_url(client):
    response = client.get(reverse('password_reset'))
    assert response.status_code == 200


# Dostępność potwierdzenia resetowania hasła
@pytest.mark.django_db
def test_password_reset_done_url(client):
    response = client.get(reverse('password_reset_done'))
    assert response.status_code == 200


# Dostępność potwierdzenia resetowania hasła z linkiem
@pytest.mark.django_db
def test_password_reset_confirm_url(client):
    response = client.get(reverse('password_reset_confirm', args=['uidb64', 'token']))
    assert response.status_code == 200


# Dostępność potwierdzenia zresetowania hasła
@pytest.mark.django_db
def test_password_reset_complete_url(client):
    response = client.get(reverse('password_reset_complete'))
    assert response.status_code == 200
