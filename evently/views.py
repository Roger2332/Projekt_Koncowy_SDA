from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EventForm, CreateUserForm

from .models import Status


# Create your views here.

def hello(request):
    return HttpResponse('Hello World!')


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Przypisz aktualnie zalogowanego użytkownika jako właściciela wydarzenia
            form.instance.author = request.user

            form.save()
            return redirect('index')
    else:
        form = EventForm()
    return render(request, 'form.html', {'form': form})


class UserCreationView(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('hello')
