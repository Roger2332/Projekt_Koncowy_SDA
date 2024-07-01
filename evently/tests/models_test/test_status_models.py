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
def test_default_status_negative():
    long_name = "BadName" * 50
    try:
        Status.objects.create(name=long_name) # próba robienia złej nazwy
    except ValidationError as e:
        pytest.fail(f"ValidationError was raised unexpectedly: {e}")