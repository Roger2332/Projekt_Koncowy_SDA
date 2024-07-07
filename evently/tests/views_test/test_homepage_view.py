import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    return Client()

# # Sprawdzenie poprawności szablonu HTML
@pytest.mark.django_db
def test_homepage_tenplate(client):
    url = reverse('homepage')
    response = client.get(url)
    assert response.status_code == 200
    assert 'homepage.html' in [template.name for template in
                               response.templates]
