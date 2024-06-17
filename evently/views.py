from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EventForm, CreateUserForm, CategoryForm

from .models import Status, Category, Event


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
    success_url = reverse_lazy('index')


class CreateCategoryView(CreateView):
    template_name = 'form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('index')

def list_events(request):
    events = Event.objects.all().order_by('start_at')
    return render(request, 'event_list.html', {'events': events})
