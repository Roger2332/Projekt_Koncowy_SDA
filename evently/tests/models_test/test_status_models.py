import pytest
import time

from django.core.exceptions import ValidationError
from django.utils import timezone

from evently.models import Status


@pytest.mark.django_db
def test_default_status_positive():
    status1 = Status.objects.create(name='Active')
    status2 = Status.objects.create(name='Inactive')
    status3 = Status.objects.create(name='Inactive')
    assert status1.name == 'Active'
    assert status2.name == 'Inactive'
    assert status3.name == 'Inactive'
    assert status1.added <= timezone.now()
    assert status1.modified <= timezone.now()


@pytest.mark.django_db
def test_long_status():
    # próba robienia złej nazwy o dlugosci 51
    try:
        status1 = Status(name="B" * 51)
        status1.full_clean()
    except ValidationError:
        pass
    else:
        status1.save()
    assert not Status.objects.filter(name="B" * 51).exists()

    # próba robienia innej nazwy niz w choice
    try:
        status2 = Status(name='Test')
        status2.full_clean()
    except ValidationError:
        pass

    else:
        status2.save()

    assert not Status.objects.filter(name='Test').exists()

    # próba robienia Dobrej nazwy
    try:
        status2 = Status(name='Active')
        status2.full_clean()
    except ValidationError:
        pass
    else:
        status2.save()

    assert Status.objects.filter(name='Active').exists()

