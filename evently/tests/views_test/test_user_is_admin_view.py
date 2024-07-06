import pytest
from django.test import Client
from evently.models import CreateUserModel


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')


@pytest.fixture
def admin():
    return CreateUserModel.objects.create_superuser(username='admin', email='admin@gmai.com', password='admin12345')


# Czy admin ma uprawnienia superusera
@pytest.mark.django_db
def test_user_is_admin_positive(admin, client):
    logged_in = client.login(username='admin', password='admin12345')
    assert logged_in
    assert admin.is_superuser


# Czy user nie ma uprawnień superusera
@pytest.mark.django_db
def test_user_is_admin_negative(client, user):
    logged_in = client.login(username='testuser', password='12345')
    assert logged_in
    assert not user.is_superuser


# Admin (superuser) ma ustawioną flagę is_superuser, niezależnie od stanu zalogowania
@pytest.mark.django_db
def test_admin_is_not_logged_in(client, admin):
    assert admin.is_superuser


# Zwykły użytkownik nie ma ustawionej flagi is_superuser, niezależnie od stanu zalogowania
@pytest.mark.django_db
def test_user_is_not_logged_in(client, user):
    assert not user.is_superuser
