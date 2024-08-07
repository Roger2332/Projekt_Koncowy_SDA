import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

# Tworzenie użytkownika przez administratora za pomocą formularza
@pytest.mark.django_db
def test_user_create_view(client, admin_user):  # Przyjmujemy admin_user, ale można użyć dowolnego użytkownika
    client.force_login(admin_user)  # Logowanie użytkownika (tutaj admina) przed wykonaniem testu
    initial_user_count = get_user_model().objects.count()  # Początkowa liczba użytkowników w bazie danych
    form_data = {
        'username': 'newuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'email': 'newuser@example.com',
    }
    # Symulacja wysłania formularza POST do widoku UserCreateView
    response = client.post(reverse('user'), form_data)
    # Sprawdzenie, czy użytkownik został dodany poprzez sprawdzenie zmiany liczby użytkowników w bazie danych
    assert get_user_model().objects.count() == initial_user_count + 1
    # Sprawdzenie, czy nastąpiło przekierowanie po dodaniu użytkownika
    assert response.status_code == 302
    assert response.url == reverse('login')