import pytest
from evently.forms import CreateUserForm
from evently.models import CreateUserModel


@pytest.fixture
def form_data():
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }


@pytest.mark.django_db
def test_create_user_form_valid(form_data):
    form = CreateUserForm(data=form_data)
    assert form.is_valid()

    user = form.save()
    assert user.first_name == form_data['first_name']
    assert user.last_name == form_data['last_name']
    assert user.username == form_data['username']
    assert user.email == form_data['email']


@pytest.mark.django_db
def test_create_user_form_invalid_duplicate_email(form_data):
    # Tworzenie istniejącego użytkownika z tym samym emailem
    CreateUserModel.objects.create_user(
        username='existinguser',
        email=form_data['email'],
        password=form_data['password1']
    )

    form = CreateUserForm(data=form_data)
    assert not form.is_valid()

    assert 'email' in form.errors
    assert form.errors['email'] == ['User with this Email already exists.']


@pytest.mark.django_db
def test_create_user_form_invalid_duplicate_email(form_data):
    # Tworzenie istniejącego użytkownika z ta sama nazwa
    CreateUserModel.objects.create_user(
        username=form_data['username'],
        email='user@gmail.com',
        password=form_data['password1']
    )

    form = CreateUserForm(data=form_data)
    assert not form.is_valid()

    assert 'username' in form.errors
    assert form.errors['username'] == ['User with this Username already exists.']
