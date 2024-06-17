from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError


class CreateUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)


class Status(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    name = models.CharField(choices=STATUS_CHOICES, max_length=50, default=STATUS_CHOICES[1][0])
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

class Event(models.Model):
    author = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    start_at = models.DateField()
    end_at = models.DateField()
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Event: {self.name}, start at: {self.start_at}, end at: {self.end_at}'


class Comment(models.Model):
    author = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField()
    event_date = models.DateTimeField(auto_now_add=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Author: {self.author}, Event: {self.event}'


class Subscription(models.Model):
    user = models.ForeignKey(CreateUserModel, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User: {self.user}, Event: {self.event}'

    # sprawdzanie, czy user nie podpisuje się na własny event
    def clean(self):
        if self.user == self.event.author:
            raise ValidationError("You cannot sign up for your own event.")
    # sprawdzanie, czy user nie jest już podpisany na event
        if Subscription.objects.filter(user=self.user, event=self.event).exists():
            raise ValidationError("You are already subscribed to this event.")


    # sprawdzanie na unikatowość
    class Meta:
        unique_together = ('user', 'event')


class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Event: {self.event}, Category: {self.category}'
