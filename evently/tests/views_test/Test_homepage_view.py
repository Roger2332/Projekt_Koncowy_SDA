import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_homepage_tenplate(client):
    url = reverse('homepage') # Uzyskanie adresu URL widoku strony głównej.
    response = client.get(url)
    assert response.status_code == 200 # Czy otwiera się prawidłowo
    assert 'homepage.html' in [template.name for template in response.templates] # Sprawdzenie poprawności szablonu HTML
