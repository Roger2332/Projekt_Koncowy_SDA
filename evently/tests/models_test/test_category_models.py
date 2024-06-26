import time

import pytest
from django.utils import timezone
from evently.models import Category


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Test Category")
    assert category.name == "Test Category"
    assert category.added <= timezone.now()
    assert category.modified <= timezone.now()


@pytest.mark.django_db
def test_modify_category():
    category = Category.objects.create(name="Test Category")
    original_added = category.added
    original_modified = category.modified
    time.sleep(1)
    category.name = "Updated Category"
    category.save()

    category.refresh_from_db()
    assert category.name == "Updated Category"
    assert category.added == original_added
    assert category.modified > original_modified


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Test Category")
    assert str(category) == "Test Category"
