import time

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from evently.models import Category


# Nowa kategoria i sprawdzanie jej poprawnośći
@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Test Category")
    assert category.name == "Test Category"
    assert category.added <= timezone.now()
    assert category.modified <= timezone.now()


# Modyfikacja kategorii i sprawdzanie zmian
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


# Tekstowa reprezentacja kategorii
@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Test Category")
    assert str(category) == "Test Category"


# Ograniczenie długości nazwy kategorii
@pytest.mark.django_db
def test_category_long():
    #Wprowadzenie za dlugiej kategori
    category = Category(name='L' *101)
    try:
        category.full_clean()
    except ValidationError:
        pass
    else:
        category.save()
    assert not Category.objects.filter(name='L' * 101).exists()
    #Wprowadzenie za poprawnej dlugosci kategori
    category = Category(name='L' * 100)
    try:
        category.full_clean()
    except ValidationError:
        pass
    else:
        category.save()
    assert Category.objects.filter(name='L' * 100).exists()