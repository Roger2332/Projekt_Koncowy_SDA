import pytest
from django.urls import reverse
from django.test import Client
from evently.models import CreateUserModel, Category


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')


@pytest.fixture
def admin():
    return CreateUserModel.objects.create_superuser(username='admin', email='admin@gmai.com', password='admin12345')


# Czy administrator ma prawo tworzyć kategorie
@pytest.mark.django_db
def test_admin_create_category_positive(admin, client):
    client.force_login(admin)
    assert admin.is_superuser  # Czy ma role superusera
    url = reverse("create_category")
    response = client.get(url)  # BLAD CLIENT - ADMIN
    assert response.status_code == 200  # Czy ma dostęp administrator
    category = Category.objects.create(
        name='Nazwa nowej kategorii'
    )
    assert category.name == 'Nazwa nowej kategorii'


# Czy user ma prawo tworzyć kategorie
@pytest.mark.django_db
def test_user_create_category_negative(user, client):
    client.force_login(user)
    assert not user.is_superuser
    url = reverse("create_category")
    response = client.get(url)  # BLAD CLIENT - ADMIN
    assert response.status_code == 403  # Czy ma dostęp wgl. do strony


# Tworzenie kategorii przez niezalogowanego użytkownika
@pytest.mark.django_db
def test_unauthenticated_user_create_category_open(client):
    url = reverse("create_category")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))  # Czy następuje przekierowanie na stronę logowania
