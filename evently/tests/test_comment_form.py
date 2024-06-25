import pytest
from django import forms
from django.forms import ModelForm

from evently.forms import CommentForm
from evently.models import Comment

@pytest.fixture
def valid_comment_data():
    return {
        'content': 'This is a valid comment content.'
    }

@pytest.fixture
def invalid_comment_data():
    return {
        'content': ''
    }

@pytest.fixture
def comment_form():
    return CommentForm()

@pytest.mark.django_db
def test_comment_form_valid(valid_comment_data, comment_form):
    form = CommentForm(data=valid_comment_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_comment_form_invalid(invalid_comment_data, comment_form):
    form = CommentForm(data=invalid_comment_data)
    assert not form.is_valid()
    assert 'content' in form.errors

@pytest.mark.django_db
def test_comment_form_widgets(comment_form):
    assert isinstance(comment_form.fields['content'].widget, forms.Textarea)
    assert 'rows' in comment_form.fields['content'].widget.attrs
    assert 'placeholder' in comment_form.fields['content'].widget.attrs

@pytest.mark.django_db
def test_comment_form_model_association(comment_form):
    expected_attrs = {'rows': 3, 'placeholder': 'Add a comment...'}
    actual_attrs = comment_form.fields['content'].widget.attrs

    assert isinstance(comment_form, ModelForm)
    assert comment_form._meta.model == Comment
    assert comment_form._meta.fields == ['content']
    assert actual_attrs['rows'] == expected_attrs['rows']
    assert actual_attrs['placeholder'] == expected_attrs['placeholder']
