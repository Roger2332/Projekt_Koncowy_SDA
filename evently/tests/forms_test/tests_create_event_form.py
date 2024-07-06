import pytest
from evently.forms import CreateEventForm
from evently.models import Category
from django.utils import timezone
from datetime import timedelta

# Poprawność danych
@pytest.mark.django_db
def test_create_event_form_valid_data():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'name': 'Test Event',
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': (timezone.now() + timedelta(days=1)).date(),
        'description': 'This is a test description for the event.',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert form.is_valid()


# Forma validacji po podaniu błędnych danych
@pytest.mark.django_db
def test_create_event_form_invalid_start_end_dates():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'name': 'Test Event',
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': timezone.now().date(),
        'description': 'This is a test description for the event.',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'The end date must be later than the start date' in form.errors['__all__']


# Formularz tworzenia wydarzenia bez podania nazwy.
@pytest.mark.django_db
@pytest.mark.django_db
def test_create_event_form_missing_name():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': (timezone.now() + timedelta(days=1)).date(),
        'description': 'This is a test description for the event.',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors


# Formularz tworzenia wydarzenia z nieprawidłową kategorią
@pytest.mark.django_db
def test_create_event_form_invalid_category():
    form_data = {
        'name': 'Test Event',
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': (timezone.now() + timedelta(days=1)).date(),
        'description': 'This is a test description for the event.',
        'category': 999  # Non-existent category ID
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'category' in form.errors

# Formularz tworzenia wydarzenia z krótkim opisem
@pytest.mark.django_db
def test_create_event_form_description_too_short():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'name': 'Test Event',
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': (timezone.now() + timedelta(days=1)).date(),
        'description': 'Short',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'description' in form.errors


# Formularz tworzenia wydarzenia z nazwą, która jest zbyt krótka.
@pytest.mark.django_db
def test_create_event_form_name_too_short():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'name': '         ',
        'place': 'Test Place',
        'start_at': timezone.now().date(),
        'end_at': (timezone.now() + timedelta(days=1)).date(),
        'description': 'This is a test description for the event.',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors


# Formularz tworzenia wydarzenia z nieprawidłową datą rozpoczęcia.
@pytest.mark.django_db
def test_create_event_form_valid_data():
    category = Category.objects.create(name='Test Category')
    form_data = {
        'name': 'Test Event',
        'place': 'Test Place',
        'start_at': (timezone.now() - timedelta(days=5)).date(),
        'end_at': timezone.now(),
        'description': 'This is a test description for the event.',
        'category': category.id
    }
    form = CreateEventForm(data=form_data)
    assert not form.is_valid()
    assert 'start_at' in form.errors
