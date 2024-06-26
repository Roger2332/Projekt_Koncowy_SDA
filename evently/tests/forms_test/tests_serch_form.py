import pytest
from datetime import date
from evently.forms import EventSearchForm
from evently.models import Event, Category, CreateUserModel, Status
from django.db import models

@pytest.fixture
def sample_categories():
    # Tworzenie przykładowych obiektów Category do testów
    category1 = Category.objects.create(name='Kategoria 1')
    category2 = Category.objects.create(name='Kategoria 2')
    return [category1, category2]

@pytest.fixture
def sample_organizers():
    # Tworzenie przykładowych obiektów CreateUserModel do testów
    organizer1 = CreateUserModel.objects.create(username='organizer1', email='organizer1@example.com')
    organizer2 = CreateUserModel.objects.create(username='organizer2', email='organizer2@example.com')
    return [organizer1, organizer2]
@pytest.fixture
def sample_statuses():
    status1 = Status.objects.create(name='Active')
    status2 = Status.objects.create(name='Inactive')
    return (status1, status2)
@pytest.fixture
def sample_events(sample_organizers, sample_statuses):
    # Tworzenie przykładowych obiektów Event do testów
    event1 = Event.objects.create(name='Wydarzenie 1', place='Miejsce A', start_at=date(2024, 7, 1),
                                  end_at=date(2024, 7, 2), author=sample_organizers[0], status_id=sample_statuses[0].id)
    event2 = Event.objects.create(name='Wydarzenie 2', place='Miejsce B', start_at=date(2024, 8, 1),
                                  end_at=date(2024, 8, 2), author=sample_organizers[1], status_id=sample_statuses[1].id)
    return [event1, event2]

@pytest.mark.django_db
def test_event_search_form_valid(sample_categories, sample_organizers):
    # Test poprawnych danych dla EventSearchForm
    form_data = {
        'query': 'Wydarzenie',
        'search_type': 'future',
        'place': 'Miejsce A',
        'category': sample_categories[0].id,
        'organizer': sample_organizers[1].id,
        'start_at': '2024-07-01',
        'end_at': '2024-07-02'
    }
    form = EventSearchForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_event_search_form_invalid(sample_categories, sample_organizers):
    # Test niepoprawnych danych dla EventSearchForm
    form_data = {
        'query': 'Wydarzenie',
        'search_type': 'invalid_type',  # Niepoprawny wybór
        'place': 'Miejsce A',
        'category': sample_categories[0].id,
        'organizer': sample_organizers[0].id,
        'start_at': '2024-07-01',
        'end_at': '2024-07-02'
    }
    form = EventSearchForm(data=form_data)
    assert not form.is_valid()
    assert 'search_type' in form.errors

@pytest.mark.django_db
def test_event_search_form_place_queryset(sample_events):
    # Testowanie zapytania queryset dla pola 'place' na podstawie obiektów Event
    form = EventSearchForm()
    place_choices = form.fields['place'].queryset.values_list('place', flat=True)
    assert set(place_choices) == {'Miejsce A', 'Miejsce B'}

@pytest.mark.django_db
def test_event_search_form_empty_data(sample_categories, sample_organizers):
    # Test pustych danych wejściowych dla EventSearchForm
    form_data = {}
    form = EventSearchForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_event_search_form_organizer_queryset(sample_organizers):
    # Testowanie poprawności queryset dla pola organizer w EventSearchForm
    form = EventSearchForm()
    organizer_choices = form.fields['organizer'].queryset.values_list('id', flat=True)
    assert set(organizer_choices) == {sample_organizers[0].id, sample_organizers[1].id}


