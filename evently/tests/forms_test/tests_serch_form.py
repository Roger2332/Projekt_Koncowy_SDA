import pytest
from datetime import date
from evently.forms import EventSearchForm
from evently.models import Event, Category, CreateUserModel, Status


# Tworzenie przykładowych obiektów Category do testów
@pytest.fixture
def sample_categories():
    category1 = Category.objects.create(name='Kategoria 1')
    category2 = Category.objects.create(name='Kategoria 2')
    return [category1, category2]


# Tworzenie przykładowych obiektów CreateUserModel do testów
@pytest.fixture
def sample_organizers():
    organizer1 = CreateUserModel.objects.create(username='organizer1', email='organizer1@example.com')
    organizer2 = CreateUserModel.objects.create(username='organizer2', email='organizer2@example.com')
    return [organizer1, organizer2]


# Tworzenie statusó w BD
@pytest.fixture
def sample_statuses():
    status1 = Status.objects.create(name='Active')
    status2 = Status.objects.create(name='Inactive')
    return (status1, status2)


# Tworzenie przykładowych obiektów Event do testów
@pytest.fixture
def sample_events(sample_organizers, sample_statuses):
    event1 = Event.objects.create(name='Wydarzenie 1', place='Miejsce A', start_at=date(2024, 7, 1),
                                  end_at=date(2024, 7, 2), author=sample_organizers[0], status_id=sample_statuses[0].id)
    event2 = Event.objects.create(name='Wydarzenie 2', place='Miejsce B', start_at=date(2024, 8, 1),
                                  end_at=date(2024, 8, 2), author=sample_organizers[1], status_id=sample_statuses[1].id)
    return [event1, event2]


# Poprawność danych dla EventSearchForm
@pytest.mark.django_db
def test_event_search_form_valid(sample_categories, sample_organizers):
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


# Test niepoprawnych danych dla EventSearchForm
@pytest.mark.django_db
def test_event_search_form_invalid(sample_categories, sample_organizers):
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


# Puste dane wejściowe dla EventSearchForm
@pytest.mark.django_db
def test_event_search_form_empty_data(sample_categories, sample_organizers):
    form_data = {}
    form = EventSearchForm(data=form_data)
    assert form.is_valid()


# Poprawność queryset dla pola organizer w EventSearchForm
@pytest.mark.django_db
def test_event_search_form_organizer_queryset(sample_organizers):
    form = EventSearchForm()
    organizer_choices = form.fields['organizer'].queryset.values_list('id', flat=True)
    assert set(organizer_choices) == {sample_organizers[0].id, sample_organizers[1].id}
