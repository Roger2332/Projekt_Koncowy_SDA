from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EventForm, CreateUserForm, CategoryForm

from .models import Status, Category, Event


@login_required  # Dekorator Sprawedza czy uzytkownik jest zalogowany, jesli nie jest zostanie przekierowany na strone do logowania
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Przypisz aktualnie zalogowanego użytkownika jako właściciela wydarzenia
            form.instance.author = request.user

            form.save()
            return redirect('list_events')
    else:
        form = EventForm()
    return render(request, 'form.html', {'form': form})


# Widok umozliwiajacy tworzenie uzytkownikow
class UserCreationView(CreateView):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('list_events')


# Widok umozliwiajacy tworzenie Kategori
class CreateCategoryView(CreateView):
    template_name = 'form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('list_events')


# Widok tworzacy liste Eventow
def list_events(request):
    events = Event.objects.all().order_by('start_at')
    return render(request, 'event_list.html', {'events': events})
