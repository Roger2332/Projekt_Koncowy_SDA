from datetime import date
import time
import pytest
from django.core.exceptions import ValidationError

from evently.models import Event, Category, CreateUserModel, Status


@pytest.mark.django_db
def test_pozitive_event_model():
    category = Category.objects.create(name='Event Category')
    status = Status.objects.create(name='Event Status')
    user = CreateUserModel.objects.create(username='Event User', email='user@email.com')
    user2 = CreateUserModel.objects.create(username='Event User2', email='user2@email.com')
    event = Event.objects.create(

        name="Event Name",
        place="Event Location",
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )
    event.category.add(category)
    event.participants.add(user2)

    assert event.name == "Event Name"
    assert event.place == "Event Location"
    assert event.start_at == date(2024, 6, 30)
    assert event.end_at == date(2024, 7, 1)
    assert event.description == "Event Description"
    assert event.category.first().name == 'Event Category'
    assert event.status == status
    assert event.author == user
    assert event.participants.count() == 1


@pytest.mark.django_db
def test_negative_event_model():
    category = Category.objects.create(name='Event Category')
    status = Status.objects.create(name='Event Status')
    status2 = Status.objects.create(name='Event fail Status')
    user = CreateUserModel.objects.create(username='Event User', email='user@email.com')
    user2 = CreateUserModel.objects.create(username='Event User2', email='user2@email.com')

    event = Event.objects.create(
        name="Event Name",
        place="Event Location",
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )

    event.category.add(category)
    event.participants.add(user2)

    assert not event.name == "Event faile"
    assert not event.place == "Event faile"
    assert not event.start_at == date(2342, 6, 30)
    assert not event.end_at == date(2342, 7, 1)
    assert not event.description == "Event fail Description"
    assert not event.status == status2
    assert not event.author == user2
    assert not event.participants.count() == 4783124


@pytest.mark.django_db
def test_edit_event_model():
    category = Category.objects.create(name='Event Category')
    status = Status.objects.create(name='Event Status')
    user = CreateUserModel.objects.create(username='Event User', email='user@email.com')
    user2 = CreateUserModel.objects.create(username='Event User2', email='user2@email.com')
    event = Event.objects.create(

        name="Event Name",
        place="Event Location",
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )
    event.category.add(category)
    event.participants.add(user2)

    original_added = event.added
    original_modified = event.modified
    time.sleep(1)
    event.name = "Updated Event"
    event.save()
    assert event.name == "Updated Event"
    assert event.added == original_added
    assert event.modified > original_modified


@pytest.mark.django_db
def test_long_name_and_place_event():
    # Test wprowadzenia za dlugiej nazwy wydarzenia
    status = Status.objects.create(name='Event Status')
    user = CreateUserModel.objects.create(username='Event User', email='user@email.com')
    long_name = "L" * 101
    event = Event(

        name=long_name,
        place="Event Location",
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )
    try:
        event.full_clean()
    except ValidationError:
        pass
    else:
        event.save()
    assert not Event.objects.filter(name=long_name).exists()

    # Test wprowadzenia za dlugiej nazwy miejsca
    event = Event(

        name="Test event",
        place=long_name,
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )
    try:
        event.full_clean()
    except ValidationError:
        pass
    else:
        event.save()
    assert not Event.objects.filter(place=long_name).exists()

    # Test wprowadzenia za Poprawnej nazwy i miejsca
    event = Event(

        name="Test event",
        place="Test miejsca",
        start_at=date(2024, 6, 30),
        end_at=date(2024, 7, 1),
        description="Event Description",
        status=status,
        author=user,
    )
    try:
        event.full_clean()
    except ValidationError:
        pass
    else:
        event.save()
    assert Event.objects.filter(name="Test event", place="Test miejsca").exists()
