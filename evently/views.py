from msilib.schema import ListView

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreateUserForm


def hello(request):
    return HttpResponse('Hello World!')


class CreateUserViews(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('hello')
