import pytest
from django.urls import reverse
from django.test import Client
from evently.models import CreateUserModel


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return CreateUserModel.objects.create_user(username='testuser', email='user1@gmail.com', password='12345')


# Czy user może wejść na swój profile,a sprawdzanie poprawnoąci HTML
@pytest.mark.django_db
def test_user_open_profile_page_positive(user, client):
    client.force_login(user)
    url = reverse("user_profile")
    response = client.get(url)
    assert response.status_code == 200
    assert 'profile.html' in [template.name for template in response.templates]


# Czy niezalogowany użytkownik może wejść na profile, czy jest dalej przekierowany na stronę logowania
def test_unauthenticated_user_open_profile(client):
    url = reverse("user_profile")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))  # Czy następuje przekierowanie na stronę logowania
