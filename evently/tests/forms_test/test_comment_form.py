import pytest
from django import forms
from django.forms import ModelForm

from evently.forms import CommentForm
from evently.models import Comment

# Fixture zwracający poprawne dane dla formularza komentarza
@pytest.fixture
def valid_comment_data():
    return {
        'content': 'This is a valid comment content.'
    }


# Fixture zwracający niepoprawne dane dla formularza komentarza (puste pole content)
@pytest.fixture
def invalid_comment_data():
    return {
        'content': ''
    }


# Fixture zwracający instancję CommentForm
@pytest.fixture
def comment_form():
    return CommentForm()


# Test sprawdzający poprawność formularza komentarza dla poprawnych danych
@pytest.mark.django_db
def test_comment_form_valid(valid_comment_data, comment_form):
    form = CommentForm(data=valid_comment_data)
    assert form.is_valid()


# Test sprawdzający niepoprawność formularza komentarza dla niepoprawnych danych
@pytest.mark.django_db
def test_comment_form_invalid(invalid_comment_data, comment_form):
    form = CommentForm(data=invalid_comment_data)
    assert not form.is_valid()
    assert 'content' in form.errors


# Test sprawdzający właściwości widgetów formularza komentarza
@pytest.mark.django_db
def test_comment_form_widgets(comment_form):
    assert isinstance(comment_form.fields['content'].widget, forms.Textarea)
    assert 'rows' in comment_form.fields['content'].widget.attrs
    assert 'placeholder' in comment_form.fields['content'].widget.attrs


# Test sprawdzający powiązanie formularza komentarza z modelem Comment
@pytest.mark.django_db
def test_comment_form_model_association(comment_form):
    expected_attrs = {'rows': 3, 'placeholder': 'Add a comment...'}
    actual_attrs = comment_form.fields['content'].widget.attrs
    assert isinstance(comment_form, ModelForm)  # Upewnienie się, że formularz jest podklasą ModelForm
    assert comment_form._meta.model == Comment  # Sprawdzenie czy model powiązany z formularzem to Comment
    assert comment_form._meta.fields == ['content']  # Sprawdzenie czy pola formularza są zgodne z modelem
    assert actual_attrs['rows'] == expected_attrs['rows']  # Sprawdzenie atrybutu 'rows' widgetu
    assert actual_attrs['placeholder'] == expected_attrs['placeholder']  # Sprawdzenie atrybutu 'placeholder' widgetu
