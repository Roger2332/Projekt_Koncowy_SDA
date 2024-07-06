import pytest
from evently.models import CreateUserModel
from django.db import IntegrityError


# Tworzenie użytkownika i sprawdzanie jego danych
@pytest.mark.django_db
def test_create_user():
    user = CreateUserModel.objects.create(
        email='user@gmail.com',
        password='12345',
        first_name='Piotr',
        last_name='Hyszko',
        username='user'
    )
    assert user is not None
    assert user.email == 'user@gmail.com'
    assert user.first_name == 'Piotr'
    assert user.last_name == 'Hyszko'
    assert user.username == 'user'
    assert user.is_superuser is False


# Tworzenie superuser i sprawdzanie jego uprawnień
@pytest.mark.django_db
def test_create_user_is_superuser():
    user2 = CreateUserModel.objects.create_superuser(
        email='user2@gmail.com',
        password='12345',
        first_name='Piotr',
        last_name='Hyszko',
        username='user',
    )
    assert user2 is not None
    assert user2.email == 'user2@gmail.com'
    assert user2.first_name == 'Piotr'
    assert user2.last_name == 'Hyszko'
    assert user2.username == 'user'
    assert user2.is_superuser is True


# Tworzenie użytkownika z zduplikowanym adresem e-mail, oczekiwanie na IntegrityError
@pytest.mark.django_db
def test_create_user_duble_email():
    user1 = CreateUserModel.objects.create(
        email='user2@gmail.com',
        password='12345',
        first_name='Piotr',
        last_name='Hyszko',
        username='user',
        is_superuser=False
    )
    assert user1 is not None
    # raises służy do sprawdzenia, czy określony kod w bloku with powoduje podniesienie określonego wyjątku, w tym przypadku IntegrityError.
    with pytest.raises(IntegrityError):
        # IntegrityError blad ktory django podnosi przy porownywaniu duplikowanych nazw
        user2 = CreateUserModel.objects.create(
            email='user2@gmail.com',
            password='6743527',
            first_name='Eryk',
            last_name='Smilek',
            username='user124',
            is_superuser=False
        )


# Tworzenie użytkownika z zduplikowaną nazwą użytkownika, oczekiwanie na IntegrityError
@pytest.mark.django_db
def test_create_user_duble_username():
    user1 = CreateUserModel.objects.create(
        email='user1@gmail.com',
        password='12345',
        first_name='Piotr',
        last_name='Hyszko',
        username='user',
        is_superuser=False
    )
    assert user1 is not None
    # raises służy do sprawdzenia, czy określony kod w bloku with powoduje podniesienie określonego wyjątku, w tym przypadku IntegrityError
    with pytest.raises(IntegrityError):
        # IntegrityError blad ktory django podnosi przy porownywaniu duplikowanych nazw
        user2 = CreateUserModel.objects.create(
            email='user2@gmail.com',
            password='6743527',
            first_name='Eryk',
            last_name='Smilek',
            username='user',
            is_superuser=False
        )
